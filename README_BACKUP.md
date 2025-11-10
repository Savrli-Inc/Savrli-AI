
---

## `api/index.py` (Final Version)

```python
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import StreamingResponse, HTMLResponse
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

# Import multi-modal AI capabilities
from ai_multimodal import (
    MultiModalProcessor, FineTuningConfig, model_registry
)

# Import advanced AI tools
from tools.summarizer import Summarizer
from tools.sentiment_analysis import SentimentAnalyzer
from tools.email_drafter import EmailDrafter
from tools.workflow_automation import WorkflowAutomation

app = FastAPI()
logger = logging.getLogger("api")
logging.basicConfig(level=logging.INFO)

# ----------------------------------------------------------------------
# Configuration & OpenAI client
# ----------------------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY is not set.")
    raise RuntimeError("OPENAI_API_KEY environment variable is required")

try:
    DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    DEFAULT_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
    DEFAULT_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    DEFAULT_CONTEXT_WINDOW = int(os.getenv("DEFAULT_CONTEXT_WINDOW", "10"))
except ValueError as e:
    logger.error("Invalid env var: %s", e)
    raise RuntimeError(f"Invalid configuration: {e}")

client = OpenAI(api_key=OPENAI_API_KEY)

# In-memory conversation history
conversation_history: Dict[str, List[Dict]] = defaultdict(list)
MAX_HISTORY_PER_SESSION = int(os.getenv("MAX_HISTORY_PER_SESSION", "20"))

# ----------------------------------------------------------------------
# Plugin manager & registration + multi-modal & tools
# ----------------------------------------------------------------------
plugin_manager = PluginManager(ai_system=client)

# Initialize multi-modal processor
multimodal_processor = MultiModalProcessor(openai_client=client)

# Initialize advanced AI tools
summarizer = Summarizer()
sentiment_analyzer = SentimentAnalyzer()
email_drafter = EmailDrafter()
workflow_automation = WorkflowAutomation()

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
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    system: Optional[str] = None
    session_id: Optional[str] = None
    context_window: Optional[int] = None
    stream: Optional[bool] = False

# Multi-modal models
class VisionRequest(BaseModel):
    prompt: str
    image_url: str
    model: Optional[str] = "gpt-4-vision-preview"
    max_tokens: Optional[int] = 1000
    session_id: Optional[str] = None

class ImageGenerationRequest(BaseModel):
    prompt: str
    n: Optional[int] = 1
    size: Optional[str] = "1024x1024"
    quality: Optional[str] = "standard"
    model: Optional[str] = "dall-e-3"
    session_id: Optional[str] = None

class AudioRequest(BaseModel):
    audio_url: str
    model: Optional[str] = "whisper-1"
    language: Optional[str] = None

class FineTuningRequest(BaseModel):
    model: str
    training_file: str
    validation_file: Optional[str] = None
    n_epochs: Optional[int] = 3
    batch_size: Optional[int] = None
    learning_rate_multiplier: Optional[float] = None
    suffix: Optional[str] = None

# AI Tools
class SummarizeRequest(BaseModel):
    text: str
    max_length: Optional[int] = 128
    style: Optional[str] = "concise"

class SentimentRequest(BaseModel):
    text: str
    detailed: Optional[bool] = False

class EmailDraftRequest(BaseModel):
    purpose: str
    recipient: Optional[str] = None
    tone: Optional[str] = "professional"
    key_points: Optional[List[str]] = None
    length: Optional[str] = "medium"
    context: Optional[str] = None

class WorkflowRequest(BaseModel):
    task_description: str
    constraints: Optional[List[str]] = None
    tools_available: Optional[List[str]] = None

# Integrations
class IntegrationMessage(BaseModel):
    plugin: str
    channel: str
    message: str
    metadata: Optional[Dict[str, Any]] = None

class WebhookPayload(BaseModel):
    plugin: str
    data: Dict[str, Any]

# ----------------------------------------------------------------------
# Core endpoint
# ----------------------------------------------------------------------
@app.post("/ai/chat")
async def chat_endpoint(request: ChatRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    max_tokens = request.max_tokens or DEFAULT_MAX_TOKENS
    if not (1 <= max_tokens <= 2000):
        raise HTTPException(status_code=400, detail="max_tokens must be between 1 and 2000")

    temperature = request.temperature or DEFAULT_TEMPERATURE
    if not (0.0 <= temperature <= 2.0):
        raise HTTPException(status_code=400, detail="temperature must be between 0.0 and 2.0")

    top_p = request.top_p
    if top_p is not None and not (0.0 <= top_p <= 1.0):
        raise HTTPException(status_code=400, detail="top_p must be between 0.0 and 1.0")

    frequency_penalty = request.frequency_penalty
    if frequency_penalty is not None and not (-2.0 <= frequency_penalty <= 2.0):
        raise HTTPException(status_code=400, detail="frequency_penalty must be between -2.0 and 2.0")

    presence_penalty = request.presence_penalty
    if presence_penalty is not None and not (-2.0 <= presence_penalty <= 2.0):
        raise HTTPException(status_code=400, detail="presence_penalty must be between -2.0 and 2.0")

    context_window = request.context_window or DEFAULT_CONTEXT_WINDOW
    if not (0 <= context_window <= 50):
        raise HTTPException(status_code=400, detail="context_window must be between 0 and 50")

    model = request.model or DEFAULT_MODEL
    session_id = request.session_id
    system_message = request.system or "You are a helpful assistant."

    messages: List[Dict] = [{"role": "system", "content": system_message}]
    if session_id and session_id in conversation_history:
        recent = conversation_history[session_id][-context_window:] if context_window > 0 else []
        messages.extend([{"role": m["role"], "content": m["content"]} for m in recent])
    messages.append({"role": "user", "content": request.prompt})

    if session_id:
        conversation_history[session_id].append({
            "role": "user",
            "content": request.prompt,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        trim_conversation_history(session_id)

    try:
        if request.stream:
            return StreamingResponse(
                stream_openai_response(model, messages, max_tokens, temperature, top_p,
                                      frequency_penalty, presence_penalty, session_id),
                media_type="text/event-stream",
            )
        else:
            return await get_complete_response(model, messages, max_tokens, temperature,
                                              top_p, frequency_penalty, presence_penalty, session_id)
    except Exception as e:
        logger.exception("OpenAI error: %s", e)
        raise HTTPException(status_code=503, detail="AI temporarily unavailable")

# ----------------------------------------------------------------------
# Non-streaming & streaming helpers
# ----------------------------------------------------------------------
async def get_complete_response(model, messages, max_tokens, temperature, top_p,
                                frequency_penalty, presence_penalty, session_id):
    def call():
        kwargs = {k: v for k, v in {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
        }.items() if v is not None}
        return client.chat.completions.create(**kwargs)
    response = await asyncio.to_thread(call)
    content = response.choices[0].message.content.strip()
    if session_id:
        conversation_history[session_id].append({
            "role": "assistant", "content": content,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        trim_conversation_history(session_id)
    return {"response": content, "session_id": session_id}

async def stream_openai_response(model, messages, max_tokens, temperature, top_p,
                                 frequency_penalty, presence_penalty, session_id):
    full = ""
    try:
        def stream():
            kwargs = {k: v for k, v in {
                "model": model, "messages": messages, "max_tokens": max_tokens,
                "temperature": temperature, "stream": True,
                "top_p": top_p, "frequency_penalty": frequency_penalty,
                "presence_penalty": presence_penalty
            }.items() if v is not None}
            return client.chat.completions.create(**kwargs)
        stream_obj = await asyncio.to_thread(stream)
        for chunk in stream_obj:
            if chunk.choices and (delta := chunk.choices[0].delta.content):
                full += delta
                yield f"data: {json.dumps({'content': delta})}\n\n"
        yield f"data: {json.dumps({'done': True})}\n\n"
        if full and session_id:
            conversation_history[session_id].append({
                "role": "assistant", "content": full,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            trim_conversation_history(session_id)
    except Exception as e:
        logger.exception("Stream error: %s", e)
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
    return {"session_id": session_id, "messages": msgs, "total_messages": len(conversation_history[session_id])}

@app.delete("/ai/history/{session_id}")
async def clear_conversation_history(session_id: str):
    if session_id in conversation_history:
        del conversation_history[session_id]
        return {"message": f"History cleared for session {session_id}"}
    return {"message": f"No history found for session {session_id}"}

# ----------------------------------------------------------------------
# Multi-Modal AI Endpoints
# ----------------------------------------------------------------------
@app.get("/ai/models")
async def list_ai_models(model_type: Optional[str] = None):
    try:
        models = multimodal_processor.list_available_models(model_type=model_type)
        return {"models": models, "count": len(models)}
    except Exception as e:
        logger.exception("Model list error: %s", e)
        raise HTTPException(status_code=500, detail="Failed to list models")

@app.get("/ai/models/{model_id}")
async def get_model_info(model_id: str):
    try:
        return multimodal_processor.get_model_info(model_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception("Model info error: %s", e)
        raise HTTPException(status_code=500, detail="Failed to get model info")

@app.post("/ai/vision")
async def analyze_image(request: VisionRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    if not request.image_url.strip():
        raise HTTPException(status_code=400, detail="Image URL cannot be empty")
    try:
        result = multimodal_processor.process_vision(
            prompt=request.prompt,
            image_url=request.image_url,
            model_id=request.model,
            max_tokens=request.max_tokens
        )
        if request.session_id:
            conversation_history[request.session_id].append({
                "role": "user", "content": f"[Image: {request.image_url}] {request.prompt}",
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            conversation_history[request.session_id].append({
                "role": "assistant", "content": result,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            trim_conversation_history(request.session_id)
        return {"response": result, "model": request.model, "session_id": request.session_id}
    except Exception as e:
        logger.exception("Vision error: %s", e)
        raise HTTPException(status_code=500, detail="Failed to process image")

@app.post("/ai/image/generate")
async def generate_image(request: ImageGenerationRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    if request.n not in [1, 2, 3, 4]:
        raise HTTPException(status_code=400, detail="n must be 1-4")
    if request.size not in ["1024x1024", "1792x1024", "1024x1792"]:
        raise HTTPException(status_code=400, detail="Invalid size")
    if request.quality not in ["standard", "hd"]:
        raise HTTPException(status_code=400, detail="quality must be standard or hd")
    try:
        response = client.images.generate(
            model=request.model,
            prompt=request.prompt,
            n=request.n,
            size=request.size,
            quality=request.quality
        )
        images = [{"url": img.url, "revised_prompt": img.revised_prompt} for img in response.data]
        if request.session_id:
            conversation_history[request.session_id].append({
                "role": "user", "content": f"[Generate: {request.prompt}]",
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            trim_conversation_history(request.session_id)
        return {"images": images, "prompt": request.prompt, "session_id": request.session_id}
    except Exception as e:
        logger.exception("Image gen error: %s", e)
        raise HTTPException(status_code=500, detail="Failed to generate image")

@app.post("/ai/audio/transcribe")
async def transcribe_audio(request: AudioRequest):
    raise HTTPException(status_code=501, detail="Audio transcription not implemented yet")

@app.post("/ai/fine-tuning/configure")
async def configure_fine_tuning(request: FineTuningRequest):
    config = FineTuningConfig(
        model_id=request.model,
        training_file=request.training_file,
        validation_file=request.validation_file,
        n_epochs=request.n_epochs or 3,
        batch_size=request.batch_size,
        learning_rate_multiplier=request.learning_rate_multiplier,
        suffix=request.suffix
    )
    is_valid, msg = config.validate()
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)
    info = multimodal_processor.get_model_info(request.model)
    if not info.get("supports_fine_tuning"):
        raise HTTPException(status_code=400, detail=f"Model {request.model} does not support fine-tuning")
    return {"success": True, "message": "Configuration validated", "config": config.to_dict()}

@app.get("/ai/models/fine-tunable")
async def list_fine_tunable_models():
    models = model_registry.list_models(supports_fine_tuning=True)
    return {"models": models, "count": len(models)}

# ----------------------------------------------------------------------
# Advanced AI Tools
# ----------------------------------------------------------------------
@app.get("/ai/tools")
async def list_ai_tools():
    return {
        "tools": [
            {"name": "summarize", "endpoint": "/ai/tools/summarize", "description": "Summarize text"},
            {"name": "sentiment", "endpoint": "/ai/tools/sentiment", "description": "Analyze sentiment"},
            {"name": "email_draft", "endpoint": "/ai/tools/email/draft", "description": "Draft emails"},
            {"name": "workflow", "endpoint": "/ai/tools/workflow/suggest", "description": "Suggest workflows"}
        ],
        "count": 4
    }

@app.post("/ai/tools/summarize")
async def summarize_text(request: SummarizeRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    if request.max_length < 10 or request.max_length > 1000:
        raise HTTPException(status_code=400, detail="max_length must be 10-1000")
    if request.style not in ["concise", "detailed", "bullet_points"]:
        raise HTTPException(status_code=400, detail="Invalid style")
    result = summarizer.summarize(request.text, request.max_length, request.style)
    return result

@app.post("/ai/tools/sentiment")
async def analyze_sentiment(request: SentimentRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    return sentiment_analyzer.analyze_sentiment(request.text, request.detailed)

@app.post("/ai/tools/email/draft")
async def draft_email(request: EmailDraftRequest):
    if not request.purpose.strip():
        raise HTTPException(status_code=400, detail="Purpose cannot be empty")
    if request.tone not in ["professional", "casual", "friendly", "formal"]:
        raise HTTPException(status_code=400, detail="Invalid tone")
    if request.length not in ["short", "medium", "long"]:
        raise HTTPException(status_code=400, detail="Invalid length")
    return email_drafter.draft_email(
        purpose=request.purpose,
        recipient=request.recipient,
        tone=request.tone,
        key_points=request.key_points,
        length=request.length,
        context=request.context
    )

@app.post("/ai/tools/workflow/suggest")
async def suggest_workflow(request: WorkflowRequest):
    if not request.task_description.strip():
        raise HTTPException(status_code=400, detail="Task description cannot be empty")
    return workflow_automation.suggest_workflow(
        task_description=request.task_description,
        constraints=request.constraints,
        tools_available=request.tools_available
    )

# ----------------------------------------------------------------------
# UI Pages
# ----------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def root():
    return {"message": "Savrli AI API is running!"}

@app.get("/playground", response_class=HTMLResponse)
async def playground():
    path = Path(__file__).parent.parent / "pages" / "playground.html"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Playground not found")
    return HTMLResponse(path.read_text(encoding="utf-8"))

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    path = Path(__file__).parent.parent / "pages" / "dashboard.html"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return HTMLResponse(path.read_text(encoding="utf-8"))

# ----------------------------------------------------------------------
# Integration Endpoints
# ----------------------------------------------------------------------
@app.get("/integrations")
async def list_integrations():
    return {"integrations": plugin_manager.list_plugins(), "count": len(plugin_manager.list_plugins())}

@app.post("/integrations/send")
async def send_integration_message(request: IntegrationMessage):
    result = plugin_manager.send_message(
        plugin_name=request.plugin,
        channel=request.channel,
        message=request.message,
        **(request.metadata or {})
    )
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Send failed"))
    return result

@app.post("/integrations/webhook")
async def process_integration_webhook(request: WebhookPayload):
    result = plugin_manager.process_webhook(request.plugin, request.data)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Webhook failed"))
    return result

@app.get("/integrations/{plugin_name}/info")
async def get_integration_info(plugin_name: str):
    plugin = plugin_manager.get_plugin(plugin_name)
    if not plugin:
        raise HTTPException(status_code=404, detail="Plugin not found")
    return plugin.get_api_info() if hasattr(plugin, "get_api_info") else {
        "plugin": plugin_name, "enabled": plugin.is_enabled(), "class": plugin.__class__.__name__
    }

# Platform-specific convenience
@app.post("/integrations/slack/send")
async def slack_send(channel: str, message: str, thread_ts: Optional[str] = None):
    metadata = {"thread_ts": thread_ts} if thread_ts else {}
    return await send_integration_message(IntegrationMessage(plugin="slack", channel=channel, message=message, metadata=metadata))

@app.post("/integrations/discord/send")
async def discord_send(channel: str, message: str, embed: Optional[Dict] = None):
    metadata = {"embed": embed} if embed else {}
    return await send_integration_message(IntegrationMessage(plugin="discord", channel=channel, message=message, metadata=metadata))

@app.post("/integrations/notion/create")
async def notion_create(page_id: str, content: str, properties: Optional[Dict] = None):
    metadata = {"operation": "create_page", "properties": properties or {}}
    return await send_integration_message(IntegrationMessage(plugin="notion", channel=page_id, message=content, metadata=metadata))

@app.post("/integrations/google-docs/create")
async def google_docs_create(title: str, content: str):
    return await send_integration_message(IntegrationMessage(plugin="google_docs", channel="new", message=content, metadata={"operation": "create_document", "title": title}))

@app.post("/integrations/google-docs/append")
async def google_docs_append(document_id: str, content: str, index: Optional[int] = None):
    metadata = {"operation": "append_text"}
    if index is not None:
        metadata["index"] = index
    return await send_integration_message(IntegrationMessage(plugin="google_docs", channel=document_id, message=content, metadata=metadata))