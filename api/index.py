from fastapi import FastAPI, HTTPException, status
from fastapi.responses import StreamingResponse, HTMLResponse, FileResponse
from pydantic import BaseModel
from openai import OpenAI
import os
import asyncio
import logging
import json
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from collections import defaultdict
from pathlib import Path

# Import plugin system
from integrations.plugin_base import PluginManager
from integrations.slack_plugin import SlackPlugin
from integrations.discord_plugin import DiscordPlugin
from integrations.notion_plugin import NotionPlugin
from integrations.google_docs_plugin import GoogleDocsPlugin

app = FastAPI()
logger = logging.getLogger("api")
logging.basicConfig(level=logging.INFO)

# ----------------------------------------------------------------------
# Configuration & OpenAI client
# ----------------------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY is not set. Set the environment variable and restart the app.")
    raise RuntimeError("OPENAI_API_KEY environment variable is required")

try:
    DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    DEFAULT_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
    DEFAULT_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    DEFAULT_CONTEXT_WINDOW = int(os.getenv("DEFAULT_CONTEXT_WINDOW", "10"))
except ValueError as e:
    logger.error("Invalid environment variable value: %s", e)
    raise RuntimeError(f"Invalid environment variable configuration: {e}")

client = OpenAI(api_key=OPENAI_API_KEY)

# In-memory conversation history (use Redis/DB in production)
conversation_history: Dict[str, List[Dict]] = defaultdict(list)
MAX_HISTORY_PER_SESSION = int(os.getenv("MAX_HISTORY_PER_SESSION", "20"))

# ----------------------------------------------------------------------
# Plugin manager & registration
# ----------------------------------------------------------------------
plugin_manager = PluginManager(ai_system=client)

# Slack
slack_config = {
    "bot_token": os.getenv("SLACK_BOT_TOKEN"),
    "signing_secret": os.getenv("SLACK_SIGNING_SECRET"),
    "enabled": os.getenv("SLACK_ENABLED", "false").lower() == "true",
}
slack_plugin = SlackPlugin(ai_system=client, config=slack_config)
if slack_config.get("bot_token"):
    plugin_manager.register_plugin("slack", slack_plugin)

# Discord
discord_config = {
    "bot_token": os.getenv("DISCORD_BOT_TOKEN"),
    "application_id": os.getenv("DISCORD_APP_ID"),
    "public_key": os.getenv("DISCORD_PUBLIC_KEY"),
    "enabled": os.getenv("DISCORD_ENABLED", "false").lower() == "true",
}
discord_plugin = DiscordPlugin(ai_system=client, config=discord_config)
if discord_config.get("bot_token"):
    plugin_manager.register_plugin("discord", discord_plugin)

# Notion
notion_config = {
    "api_token": os.getenv("NOTION_API_TOKEN"),
    "enabled": os.getenv("NOTION_ENABLED", "false").lower() == "true",
}
notion_plugin = NotionPlugin(ai_system=client, config=notion_config)
if notion_config.get("api_token"):
    plugin_manager.register_plugin("notion", notion_plugin)

# Google Docs
google_docs_config = {
    "credentials": os.getenv("GOOGLE_DOCS_CREDENTIALS"),
    "enabled": os.getenv("GOOGLE_DOCS_ENABLED", "false").lower() == "true",
}
google_docs_plugin = GoogleDocsPlugin(ai_system=client, config=google_docs_config)
if google_docs_config.get("credentials"):
    plugin_manager.register_plugin("google_docs", google_docs_plugin)


# ----------------------------------------------------------------------
# Helper
# ----------------------------------------------------------------------
def trim_conversation_history(session_id: str):
    """Trim conversation history to MAX_HISTORY_PER_SESSION messages."""
    if len(conversation_history[session_id]) > MAX_HISTORY_PER_SESSION:
        conversation_history[session_id] = conversation_history[session_id][-MAX_HISTORY_PER_SESSION:]


# ----------------------------------------------------------------------
# Pydantic models
# ----------------------------------------------------------------------
class Message(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None


class ChatRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    model: Optional[str] = None

    # Advanced OpenAI API parameters
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None

    # Custom system instruction
    system: Optional[str] = None

    # Session management
    session_id: Optional[str] = None
    context_window: Optional[int] = None

    # Enable streaming response
    stream: Optional[bool] = False


# ----------------------------------------------------------------------
# Core endpoint
# ----------------------------------------------------------------------
@app.post("/ai/chat")
async def chat_endpoint(request: ChatRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Prompt cannot be empty")

    # ---- Parameter handling & validation ----
    max_tokens = request.max_tokens if request.max_tokens is not None else DEFAULT_MAX_TOKENS
    if not (1 <= max_tokens <= 2000):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="max_tokens must be between 1 and 2000")

    temperature = request.temperature if request.temperature is not None else DEFAULT_TEMPERATURE
    if not (0.0 <= temperature <= 2.0):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="temperature must be between 0.0 and 2.0")

    # Optional advanced params
    top_p = request.top_p
    if top_p is not None and not (0.0 <= top_p <= 1.0):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="top_p must be between 0.0 and 1.0")

    frequency_penalty = request.frequency_penalty
    if frequency_penalty is not None and not (-2.0 <= frequency_penalty <= 2.0):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="frequency_penalty must be between -2.0 and 2.0")

    presence_penalty = request.presence_penalty
    if presence_penalty is not None and not (-2.0 <= presence_penalty <= 2.0):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="presence_penalty must be between -2.0 and 2.0")

    context_window = request.context_window if request.context_window is not None else DEFAULT_CONTEXT_WINDOW
    if not (0 <= context_window <= 50):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="context_window must be between 0 and 50")

    model = request.model if request.model is not None else DEFAULT_MODEL
    session_id = request.session_id

    system_message = request.system or "You are a helpful assistant providing conversational recommendations."

    # ---- Build messages list ----
    messages: List[Dict] = [{"role": "system", "content": system_message}]

    if session_id in conversation_history:
        recent = conversation_history[session_id][-context_window:] if context_window > 0 else []
        messages.extend([{"role": m["role"], "content": m["content"]} for m in recent])

    messages.append({"role": "user", "content": request.prompt})

    # ---- Store user message ----
    if session_id:
        conversation_history[session_id].append({
            "role": "user",
            "content": request.prompt,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        trim_conversation_history(session_id)

    # ---- Call OpenAI (streaming or full) ----
    try:
        if request.stream:
            return StreamingResponse(
                stream_openai_response(
                    model, messages, max_tokens, temperature,
                    top_p, frequency_penalty, presence_penalty, session_id
                ),
                media_type="text/event-stream",
            )
        else:
            return await get_complete_response(
                model, messages, max_tokens, temperature,
                top_p, frequency_penalty, presence_penalty, session_id
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error calling OpenAI: %s", e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail="AI temporarily unavailable")


# ----------------------------------------------------------------------
# Non-streaming helper
# ----------------------------------------------------------------------
async def get_complete_response(
    model: str,
    messages: List[Dict],
    max_tokens: int,
    temperature: float,
    top_p: Optional[float],
    frequency_penalty: Optional[float],
    presence_penalty: Optional[float],
    session_id: Optional[str],
):
    def call_openai():
        kwargs: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if top_p is not None:
            kwargs["top_p"] = top_p
        if frequency_penalty is not None:
            kwargs["frequency_penalty"] = frequency_penalty
        if presence_penalty is not None:
            kwargs["presence_penalty"] = presence_penalty
        return client.chat.completions.create(**kwargs)

    response = await asyncio.to_thread(call_openai)

    # Defensive parsing (same as before)
    choices = getattr(response, "choices", None)
    if not choices or len(choices) == 0:
        logger.error("OpenAI returned no choices: %s", response)
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="AI returned an empty response")

    first = choices[0]
    message = first.get("message") if isinstance(first, dict) else getattr(first, "message", None)
    content = None
    if isinstance(message, dict):
        content = message.get("content")
    elif message is not None:
        content = getattr(message, "content", None)
    if not content:
        content = first.get("text") if isinstance(first, dict) else getattr(first, "text", None)

    if not content:
        logger.error("Could not parse AI response: %s", response)
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Unexpected AI response format")

    ai_response = str(content).strip()

    if session_id:
        conversation_history[session_id].append({
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        trim_conversation_history(session_id)

    return {"response": ai_response, "session_id": session_id}


# ----------------------------------------------------------------------
# Streaming helper
# ----------------------------------------------------------------------
async def stream_openai_response(
    model: str,
    messages: List[Dict],
    max_tokens: int,
    temperature: float,
    top_p: Optional[float],
    frequency_penalty: Optional[float],
    presence_penalty: Optional[float],
    session_id: Optional[str],
):
    full_response = ""

    try:
        def create_stream():
            kwargs: Dict[str, Any] = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": True,
            }
            if top_p is not None:
                kwargs["top_p"] = top_p
            if frequency_penalty is not None:
                kwargs["frequency_penalty"] = frequency_penalty
            if presence_penalty is not None:
                kwargs["presence_penalty"] = presence_penalty
            return client.chat.completions.create(**kwargs)

        stream = await asyncio.to_thread(create_stream)

        def process_stream():
            result = []
            for chunk in stream:
                if getattr(chunk, "choices", None) and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if getattr(delta, "content", None):
                        result.append(delta.content)
            return result

        chunks = await asyncio.to_thread(process_stream)

        for content in chunks:
            full_response += content
            yield f"data: {json.dumps({'content': content})}\n\n"

        yield f"data: {json.dumps({'done': True})}\n\n"

        if full_response and session_id:
            conversation_history[session_id].append({
                "role": "assistant",
                "content": full_response,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            trim_conversation_history(session_id)

    except Exception as e:
        logger.exception("Error streaming OpenAI response: %s", e)
        yield f"data: {json.dumps({'error': 'Stream failed'})}\n\n"


# ----------------------------------------------------------------------
# History endpoints
# ----------------------------------------------------------------------
@app.get("/ai/history/{session_id}")
async def get_conversation_history(session_id: str, limit: Optional[int] = 50):
    if session_id not in conversation_history:
        return {"session_id": session_id, "messages": []}

    msgs = conversation_history[session_id]
    if limit:
        msgs = msgs[-limit:]

    return {
        "session_id": session_id,
        "messages": msgs,
        "total_messages": len(conversation_history[session_id]),
    }


@app.delete("/ai/history/{session_id}")
async def clear_conversation_history(session_id: str):
    if session_id in conversation_history:
        del conversation_history[session_id]
        return {"message": f"History cleared for session {session_id}"}
    return {"message": f"No history found for session {session_id}"}


# ----------------------------------------------------------------------
# Simple / health endpoints
# ----------------------------------------------------------------------
@app.get("/")
async def root():
    return {"message": "Savrli AI Chat API is running!"}


@app.get("/hello")
async def hello():
    return {"message": "Hello from Savrli AI!"}


@app.get("/playground", response_class=HTMLResponse)
async def playground():
    playground_path = Path(__file__).parent.parent / "pages" / "playground.html"
    if not playground_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Playground page not found")

    with open(playground_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


# ----------------------------------------------------------------------
# Integration models
# ----------------------------------------------------------------------
class IntegrationMessage(BaseModel):
    plugin: str
    channel: str
    message: str
    metadata: Optional[Dict[str, Any]] = None


class WebhookPayload(BaseModel):
    plugin: str
    data: Dict[str, Any]


# ----------------------------------------------------------------------
# Integration generic endpoints
# ----------------------------------------------------------------------
@app.get("/integrations")
async def list_integrations():
    plugins = plugin_manager.list_plugins()
    return {"integrations": plugins, "count": len(plugins)}


@app.post("/integrations/send")
async def send_integration_message(request: IntegrationMessage):
    result = plugin_manager.send_message(
        plugin_name=request.plugin,
        channel=request.channel,
        message=request.message,
        **(request.metadata or {})
    )
    if not result.get("success"):
        safe_msg = "Failed to send message"
        err = result.get("error", "")
        if any(k in str(err).lower() for k in ["not found", "disabled", "invalid", "missing", "configuration"]):
            safe_msg = str(err)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=safe_msg)

    return {
        "success": result.get("success"),
        "plugin": result.get("plugin"),
        "result": result.get("result", {}),
    }


@app.post("/integrations/webhook")
async def process_integration_webhook(request: WebhookPayload):
    result = plugin_manager.process_webhook(
        plugin_name=request.plugin,
        webhook_data=request.data,
    )
    if not result.get("success"):
        safe_msg = "Failed to process webhook"
        err = result.get("error", "")
        if any(k in str(err).lower() for k in ["not found", "disabled", "invalid", "missing", "configuration"]):
            safe_msg = str(err)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=safe_msg)

    return {
        "success": result.get("success"),
        "plugin": result.get("plugin"),
        "result": result.get("result", {}),
    }


@app.get("/integrations/{plugin_name}/info")
async def get_integration_info(plugin_name: str):
    plugin = plugin_manager.get_plugin(plugin_name)
    if not plugin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Plugin {plugin_name} not found")

    if hasattr(plugin, "get_api_info"):
        return plugin.get_api_info()

    return {
        "plugin": plugin_name,
        "enabled": plugin.is_enabled(),
        "class": plugin.__class__.__name__,
    }


# ----------------------------------------------------------------------
# Platform-specific convenience endpoints
# ----------------------------------------------------------------------
@app.post("/integrations/slack/send")
async def slack_send_message(channel: str, message: str, thread_ts: Optional[str] = None):
    metadata: Dict[str, Any] = {}
    if thread_ts:
        metadata["thread_ts"] = thread_ts
    return await send_integration_message(
        IntegrationMessage(plugin="slack", channel=channel, message=message, metadata=metadata)
    )


@app.post("/integrations/discord/send")
async def discord_send_message(channel: str, message: str, embed: Optional[Dict[str, Any]] = None):
    metadata: Dict[str, Any] = {}
    if embed:
        metadata["embed"] = embed
    return await send_integration_message(
        IntegrationMessage(plugin="discord", channel=channel, message=message, metadata=metadata)
    )


@app.post("/integrations/notion/create")
async def notion_create_page(page_id: str, content: str, properties: Optional[Dict[str, Any]] = None):
    metadata: Dict[str, Any] = {"operation": "create_page"}
    if properties:
        metadata["properties"] = properties
    return await send_integration_message(
        IntegrationMessage(plugin="notion", channel=page_id, message=content, metadata=metadata)
    )


@app.post("/integrations/google-docs/create")
async def google_docs_create_document(title: str, content: str):
    metadata = {"operation": "create_document", "title": title}
    return await send_integration_message(
        IntegrationMessage(plugin="google_docs", channel="new", message=content, metadata=metadata)
    )


@app.post("/integrations/google-docs/append")
async def google_docs_append_text(document_id: str, content: str, index: Optional[int] = None):
    metadata: Dict[str, Any] = {"operation": "append_text"}
    if index is not None:
        metadata["index"] = index
    return await send_integration_message(
        IntegrationMessage(plugin="google_docs", channel=document_id, message=content, metadata=metadata)
    )