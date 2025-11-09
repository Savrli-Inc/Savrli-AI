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

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    # Fail fast during import/startup so misconfiguration is obvious
    logger.error("OPENAI_API_KEY is not set. Set the environment variable and restart the app.")
    raise RuntimeError("OPENAI_API_KEY environment variable is required")

# Read configurable defaults from env
try:
    DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    DEFAULT_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
    DEFAULT_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    DEFAULT_CONTEXT_WINDOW = int(os.getenv("DEFAULT_CONTEXT_WINDOW", "10"))
except ValueError as e:
    logger.error("Invalid environment variable value: %s", e)
    raise RuntimeError(f"Invalid environment variable configuration: {e}")

# Create client once
client = OpenAI(api_key=OPENAI_API_KEY)

# In-memory conversation history storage (use Redis/DB in production)
# Structure: {session_id: [{"role": "user/assistant", "content": "...", "timestamp": "..."}]}
conversation_history: Dict[str, List[Dict]] = defaultdict(list)
MAX_HISTORY_PER_SESSION = int(os.getenv("MAX_HISTORY_PER_SESSION", "20"))

# Initialize plugin manager and register plugins
plugin_manager = PluginManager(ai_system=client)

# Register Slack plugin
slack_config = {
    "bot_token": os.getenv("SLACK_BOT_TOKEN"),
    "signing_secret": os.getenv("SLACK_SIGNING_SECRET"),
    "enabled": os.getenv("SLACK_ENABLED", "false").lower() == "true"
}
slack_plugin = SlackPlugin(ai_system=client, config=slack_config)
if slack_config.get("bot_token"):  # Only register if configured
    plugin_manager.register_plugin("slack", slack_plugin)

# Register Discord plugin
discord_config = {
    "bot_token": os.getenv("DISCORD_BOT_TOKEN"),
    "application_id": os.getenv("DISCORD_APP_ID"),
    "public_key": os.getenv("DISCORD_PUBLIC_KEY"),
    "enabled": os.getenv("DISCORD_ENABLED", "false").lower() == "true"
}
discord_plugin = DiscordPlugin(ai_system=client, config=discord_config)
if discord_config.get("bot_token"):  # Only register if configured
    plugin_manager.register_plugin("discord", discord_plugin)

# Register Notion plugin
notion_config = {
    "api_token": os.getenv("NOTION_API_TOKEN"),
    "enabled": os.getenv("NOTION_ENABLED", "false").lower() == "true"
}
notion_plugin = NotionPlugin(ai_system=client, config=notion_config)
if notion_config.get("api_token"):  # Only register if configured
    plugin_manager.register_plugin("notion", notion_plugin)

# Register Google Docs plugin
google_docs_config = {
    "credentials": os.getenv("GOOGLE_DOCS_CREDENTIALS"),
    "enabled": os.getenv("GOOGLE_DOCS_ENABLED", "false").lower() == "true"
}
google_docs_plugin = GoogleDocsPlugin(ai_system=client, config=google_docs_config)
if google_docs_config.get("credentials"):  # Only register if configured
    plugin_manager.register_plugin("google_docs", google_docs_plugin)

def trim_conversation_history(session_id: str):
    """Trim conversation history to MAX_HISTORY_PER_SESSION messages"""
    if len(conversation_history[session_id]) > MAX_HISTORY_PER_SESSION:
        conversation_history[session_id] = conversation_history[session_id][-MAX_HISTORY_PER_SESSION:]

class Message(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    prompt: str
    # Optional per-request overrides (validated server-side)
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    model: Optional[str] = None
    # Advanced OpenAI API parameters
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    # Custom system instruction
    system: Optional[str] = None
    # Session management for conversation history
    session_id: Optional[str] = None
    # Context window (number of previous turns to include)
    context_window: Optional[int] = None
    # Enable streaming response
    stream: Optional[bool] = False

@app.post("/ai/chat")
async def chat_endpoint(request: ChatRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Prompt cannot be empty")

    # Apply config and clamp values
    max_tokens = request.max_tokens if request.max_tokens is not None else DEFAULT_MAX_TOKENS
    # Safety: prevent extremely large token requests
    if max_tokens <= 0 or max_tokens > 2000:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="max_tokens must be between 1 and 2000")

    temperature = request.temperature if request.temperature is not None else DEFAULT_TEMPERATURE
    # Validate temperature bounds
    if temperature < 0.0 or temperature > 2.0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="temperature must be between 0.0 and 2.0")
    
    # Validate top_p if provided
    top_p = request.top_p
    if top_p is not None and (top_p < 0.0 or top_p > 1.0):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="top_p must be between 0.0 and 1.0")
    
    # Validate frequency_penalty if provided
    frequency_penalty = request.frequency_penalty
    if frequency_penalty is not None and (frequency_penalty < -2.0 or frequency_penalty > 2.0):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="frequency_penalty must be between -2.0 and 2.0")
    
    # Validate presence_penalty if provided
    presence_penalty = request.presence_penalty
    if presence_penalty is not None and (presence_penalty < -2.0 or presence_penalty > 2.0):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="presence_penalty must be between -2.0 and 2.0")
    
    # Validate context_window if provided
    context_window = request.context_window if request.context_window is not None else DEFAULT_CONTEXT_WINDOW
    if context_window < 0 or context_window > 50:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="context_window must be between 0 and 50")
    
    model = request.model if request.model is not None else DEFAULT_MODEL
    session_id = request.session_id if request.session_id else None  # None if not provided
    
    # Use custom system instruction or default
    system_message = request.system if request.system else "You are a helpful assistant providing conversational recommendations."
    
    # Build messages array with conversation history
    messages = [{"role": "system", "content": system_message}]
    
    # Add conversation history if session_id is provided
    if session_id in conversation_history:
        # Add recent history (use configurable context_window)
        recent_history = conversation_history[session_id][-context_window:] if context_window > 0 else []
        messages.extend([{"role": msg["role"], "content": msg["content"]} for msg in recent_history])
    
    # Add current user message
    messages.append({"role": "user", "content": request.prompt})
    
    # Store user message in history (only if session_id provided)
    if session_id:
        conversation_history[session_id].append({
            "role": "user",
            "content": request.prompt,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        trim_conversation_history(session_id)

    try:
        # Handle streaming vs non-streaming responses
        if request.stream:
            return StreamingResponse(
                stream_openai_response(model, messages, max_tokens, temperature, top_p, frequency_penalty, presence_penalty, session_id),
                media_type="text/event-stream"
            )
        else:
            # Non-streaming response (original behavior with history support)
            return await get_complete_response(model, messages, max_tokens, temperature, top_p, frequency_penalty, presence_penalty, session_id)

    except HTTPException:
        # Re-raise HTTPExceptions raised above
        raise
    except Exception as e:
        # Log the error for debugging, but don't leak internal details to clients
        logger.exception("Error calling OpenAI: %s", e)
        # Map to a 503 to indicate an upstream service problem
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="AI temporarily unavailable")

async def get_complete_response(model: str, messages: List[Dict], max_tokens: int, temperature: float, 
                                top_p: Optional[float], frequency_penalty: Optional[float], 
                                presence_penalty: Optional[float], session_id: str):
    """Get complete non-streaming response"""
    def call_openai():
        # Build kwargs with only non-None optional parameters
        kwargs = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        if top_p is not None:
            kwargs["top_p"] = top_p
        if frequency_penalty is not None:
            kwargs["frequency_penalty"] = frequency_penalty
        if presence_penalty is not None:
            kwargs["presence_penalty"] = presence_penalty
        
        return client.chat.completions.create(**kwargs)

    response = await asyncio.to_thread(call_openai)

    # Defensive parsing
    choices = getattr(response, "choices", None)
    if not choices or not isinstance(choices, (list, tuple)) or len(choices) == 0:
        logger.error("OpenAI returned no choices: %s", response)
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="AI returned an empty response")

    # Attempt to extract message content in a variety of shapes
    first_choice = choices[0]
    if first_choice is None:
        logger.error("OpenAI returned None for first choice: %s", response)
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Unexpected AI response format")
        
    message = first_choice.get("message") if isinstance(first_choice, dict) else getattr(first_choice, "message", None)
    content = None
    if isinstance(message, dict):
        content = message.get("content")
    elif message is not None:
        # Some SDK responses expose .content
        content = getattr(message, "content", None)

    if not content:
        # Fallback: some older SDKs put text in choices[0].text
        content = first_choice.get("text") if isinstance(first_choice, dict) else getattr(first_choice, "text", None)

    if not content:
        logger.error("Could not parse AI response: %s", response)
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Unexpected AI response format")

    # Ensure content is a string
    if not isinstance(content, str):
        content = str(content)
    
    ai_response = content.strip()
    
    # Store assistant response in history (only if session_id provided)
    if session_id:
        conversation_history[session_id].append({
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        trim_conversation_history(session_id)
    
    return {"response": ai_response, "session_id": session_id}

async def stream_openai_response(model: str, messages: List[Dict], max_tokens: int, temperature: float,
                                 top_p: Optional[float], frequency_penalty: Optional[float],
                                 presence_penalty: Optional[float], session_id: str):
    """Stream OpenAI response using Server-Sent Events"""
    full_response = ""
    
    try:
        def create_stream():
            # Build kwargs with only non-None optional parameters
            kwargs = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": True
            }
            if top_p is not None:
                kwargs["top_p"] = top_p
            if frequency_penalty is not None:
                kwargs["frequency_penalty"] = frequency_penalty
            if presence_penalty is not None:
                kwargs["presence_penalty"] = presence_penalty
            
            return client.chat.completions.create(**kwargs)
        
        # Run stream creation in thread to avoid blocking
        stream = await asyncio.to_thread(create_stream)
        
        # Process stream in thread to avoid blocking
        def process_stream():
            result = []
            for chunk in stream:
                if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, 'content') and delta.content:
                        result.append(delta.content)
            return result
        
        chunks = await asyncio.to_thread(process_stream)
        
        # Yield chunks as SSE
        for content in chunks:
            full_response += content
            yield f"data: {json.dumps({'content': content})}\n\n"
        
        # Send completion marker
        yield f"data: {json.dumps({'done': True})}\n\n"
        
        # Store complete assistant response in history (only if session_id provided)
        if full_response and session_id:
            conversation_history[session_id].append({
                "role": "assistant",
                "content": full_response,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            trim_conversation_history(session_id)
                
    except Exception as e:
        logger.exception("Error streaming OpenAI response: %s", e)
        yield f"data: {json.dumps({'error': 'Stream failed'})}\n\n"

@app.get("/ai/history/{session_id}")
async def get_conversation_history(session_id: str, limit: Optional[int] = 50):
    """Get conversation history for a session"""
    if session_id not in conversation_history:
        return {"session_id": session_id, "messages": []}
    
    messages = conversation_history[session_id]
    if limit:
        messages = messages[-limit:]
    
    return {
        "session_id": session_id,
        "messages": messages,
        "total_messages": len(conversation_history[session_id])
    }

@app.delete("/ai/history/{session_id}")
async def clear_conversation_history(session_id: str):
    """Clear conversation history for a session"""
    if session_id in conversation_history:
        del conversation_history[session_id]
        return {"message": f"History cleared for session {session_id}"}
    return {"message": f"No history found for session {session_id}"}

@app.get("/")
async def root():
    return {"message": "Savrli AI Chat API is running!"}

@app.get("/playground", response_class=HTMLResponse)
async def playground():
    """
    Serve the interactive playground/demo page
    
    This endpoint serves a static HTML page that provides an interactive UI
    for testing the Savrli AI backend capabilities. Users can:
    - Submit prompts and get instant AI responses
    - Adjust AI parameters (model, temperature, max tokens)
    - Maintain conversation history with session management
    - Test different models and configurations
    
    The playground is useful for:
    - Onboarding new users to understand AI capabilities
    - Testing API functionality in a user-friendly interface
    - Demonstrating features to stakeholders
    - Debugging and experimenting with different parameters
    """
    playground_path = Path(__file__).parent.parent / "pages" / "playground.html"
    
    if not playground_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playground page not found"
        )
    
    with open(playground_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    return HTMLResponse(content=html_content)

# ============================================================================
# Integration Endpoints
# ============================================================================

class IntegrationMessage(BaseModel):
    """Request model for sending messages via integrations"""
    plugin: str
    channel: str
    message: str
    metadata: Optional[Dict[str, Any]] = None

class WebhookPayload(BaseModel):
    """Request model for webhook processing"""
    plugin: str
    data: Dict[str, Any]

@app.get("/integrations")
async def list_integrations():
    """
    List all registered integration plugins.
    
    Returns a list of available integrations with their status.
    """
    plugins = plugin_manager.list_plugins()
    return {
        "integrations": plugins,
        "count": len(plugins)
    }

@app.post("/integrations/send")
async def send_integration_message(request: IntegrationMessage):
    """
    Send a message via a specific integration plugin.
    
    This endpoint allows sending AI-generated or custom messages
    to integrated platforms like Slack, Discord, Notion, or Google Docs.
    
    Args:
        request: Integration message request with plugin, channel, and message
        
    Returns:
        Result of the send operation
    """
    result = plugin_manager.send_message(
        plugin_name=request.plugin,
        channel=request.channel,
        message=request.message,
        **(request.metadata or {})
    )
    
    if not result.get("success"):
        # Sanitize error message to avoid stack trace exposure
        error_msg = "Failed to send message"
        if result.get("error"):
            # Only expose safe, expected error messages
            safe_errors = [
                "not found",
                "disabled",
                "invalid",
                "missing",
                "configuration"
            ]
            error_detail = str(result.get("error", "")).lower()
            if any(safe_err in error_detail for safe_err in safe_errors):
                error_msg = result.get("error", error_msg)
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )
    
    # Return only safe fields to avoid exposing internal errors
    safe_result = {
        "success": result.get("success"),
        "plugin": result.get("plugin"),
        "result": result.get("result", {})
    }
    return safe_result

@app.post("/integrations/webhook")
async def process_integration_webhook(request: WebhookPayload):
    """
    Process incoming webhooks from integration platforms.
    
    This endpoint handles webhooks from Slack, Discord, Notion,
    and Google Docs, routing them to the appropriate plugin.
    
    Args:
        request: Webhook payload with plugin identifier and data
        
    Returns:
        Processing result from the plugin
    """
    result = plugin_manager.process_webhook(
        plugin_name=request.plugin,
        webhook_data=request.data
    )
    
    if not result.get("success"):
        # Sanitize error message to avoid stack trace exposure
        error_msg = "Failed to process webhook"
        if result.get("error"):
            # Only expose safe, expected error messages
            safe_errors = [
                "not found",
                "disabled",
                "invalid",
                "missing",
                "configuration"
            ]
            error_detail = str(result.get("error", "")).lower()
            if any(safe_err in error_detail for safe_err in safe_errors):
                error_msg = result.get("error", error_msg)
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )
    
    # Return only safe fields to avoid exposing internal errors
    safe_result = {
        "success": result.get("success"),
        "plugin": result.get("plugin"),
        "result": result.get("result", {})
    }
    return safe_result

@app.get("/integrations/{plugin_name}/info")
async def get_integration_info(plugin_name: str):
    """
    Get detailed information about a specific integration plugin.
    
    Returns API endpoints, required scopes/permissions, and
    documentation links for the plugin.
    
    Args:
        plugin_name: Name of the plugin (slack, discord, notion, google_docs)
        
    Returns:
        Plugin information and documentation
    """
    plugin = plugin_manager.get_plugin(plugin_name)
    
    if not plugin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plugin {plugin_name} not found"
        )
    
    # Get plugin API info if available
    if hasattr(plugin, 'get_api_info'):
        return plugin.get_api_info()
    
    return {
        "plugin": plugin_name,
        "enabled": plugin.is_enabled(),
        "class": plugin.__class__.__name__
    }

# Platform-specific convenience endpoints

@app.post("/integrations/slack/send")
async def slack_send_message(channel: str, message: str, thread_ts: Optional[str] = None):
    """
    Send a message to Slack (convenience endpoint).
    
    Args:
        channel: Slack channel ID or name
        message: Message to send
        thread_ts: Optional thread timestamp for threaded replies
        
    Returns:
        Operation result
    """
    try:
        metadata = {}
        if thread_ts:
            metadata["thread_ts"] = thread_ts
        
        return await send_integration_message(
            IntegrationMessage(
                plugin="slack",
                channel=channel,
                message=message,
                metadata=metadata
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error in Slack send_message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send Slack message"
        )

@app.post("/integrations/discord/send")
async def discord_send_message(channel: str, message: str, embed: Optional[Dict[str, Any]] = None):
    """
    Send a message to Discord (convenience endpoint).
    
    Args:
        channel: Discord channel ID
        message: Message to send
        embed: Optional embed object
        
    Returns:
        Operation result
    """
    try:
        metadata = {}
        if embed:
            metadata["embed"] = embed
        
        return await send_integration_message(
            IntegrationMessage(
                plugin="discord",
                channel=channel,
                message=message,
                metadata=metadata
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error in Discord send_message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send Discord message"
        )

@app.post("/integrations/notion/create")
async def notion_create_page(page_id: str, content: str, properties: Optional[Dict[str, Any]] = None):
    """
    Create or update a Notion page (convenience endpoint).
    
    Args:
        page_id: Notion page or database ID
        content: Content to add
        properties: Optional page properties
        
    Returns:
        Operation result
    """
    try:
        metadata = {"operation": "create_page"}
        if properties:
            metadata["properties"] = properties
        
        return await send_integration_message(
            IntegrationMessage(
                plugin="notion",
                channel=page_id,
                message=content,
                metadata=metadata
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error in Notion create_page: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create Notion page"
        )

@app.post("/integrations/google-docs/create")
async def google_docs_create_document(title: str, content: str):
    """
    Create a new Google Docs document (convenience endpoint).
    
    Args:
        title: Document title
        content: Initial content
        
    Returns:
        Operation result with document ID
    """
    try:
        metadata = {
            "operation": "create_document",
            "title": title
        }
        
        return await send_integration_message(
            IntegrationMessage(
                plugin="google_docs",
                channel="new",
                message=content,
                metadata=metadata
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error in Google Docs create_document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create Google Docs document"
        )

@app.post("/integrations/google-docs/append")
async def google_docs_append_text(document_id: str, content: str, index: Optional[int] = None):
    """
    Append text to a Google Docs document (convenience endpoint).
    
    Args:
        document_id: Google Docs document ID
        content: Content to append
        index: Optional insert position
        
    Returns:
        Operation result
    """
    try:
        metadata = {"operation": "append_text"}
        if index is not None:
            metadata["index"] = index
        
        return await send_integration_message(
            IntegrationMessage(
                plugin="google_docs",
                channel=document_id,
                message=content,
                metadata=metadata
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error in Google Docs append_text: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to append text to Google Docs document"
        )
