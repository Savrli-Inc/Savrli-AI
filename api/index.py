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

# Import multi-modal AI capabilities
from ai_multimodal import (
    MultiModalProcessor, FineTuningConfig, ModelType,
    model_registry
)

# Import advanced AI tools
from tools.summarizer import Summarizer
from tools.sentiment_analysis import SentimentAnalyzer
from tools.email_drafter import EmailDrafter
from tools.workflow_automation import WorkflowAutomation

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

# Initialize multi-modal processor
multimodal_processor = MultiModalProcessor(openai_client=client)

# Initialize advanced AI tools
summarizer = Summarizer()
sentiment_analyzer = SentimentAnalyzer()
email_drafter = EmailDrafter()
workflow_automation = WorkflowAutomation()


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

@app.get("/hello")
async def hello():
    """
    Simple hello endpoint for testing and health checks.
    
    Returns a friendly greeting message to confirm the API is responsive.
    This endpoint requires no authentication and can be used for:
    - Basic health checks
    - API availability testing
    - Quick connectivity verification
    """
    return {"message": "Hello from Savrli AI!"}

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

# ============================================================================
# Multi-Modal AI Endpoints
# ============================================================================

class VisionRequest(BaseModel):
    """Request model for vision/image analysis"""
    prompt: str
    image_url: str
    model: Optional[str] = "gpt-4-vision-preview"
    max_tokens: Optional[int] = 1000

class AudioRequest(BaseModel):
    """Request model for audio transcription"""
    audio_url: str
    model: Optional[str] = "whisper-1"
    language: Optional[str] = None

class FineTuningRequest(BaseModel):
    """Request model for fine-tuning configuration"""
    model: str
    training_file: str
    validation_file: Optional[str] = None
    n_epochs: Optional[int] = 3
    batch_size: Optional[int] = None
    learning_rate_multiplier: Optional[float] = None
    suffix: Optional[str] = None

@app.get("/ai/models")
async def list_ai_models(model_type: Optional[str] = None):
    """
    List all available AI models with optional filtering by type.
    
    Query Parameters:
        model_type: Optional filter by type (text, vision, audio, multimodal)
    
    Returns:
        List of available models with their capabilities
    """
    try:
        models = multimodal_processor.list_available_models(model_type=model_type)
        return {
            "models": models,
            "count": len(models)
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Error listing models: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list models"
        )

@app.get("/ai/models/{model_id}")
async def get_model_info(model_id: str):
    """
    Get detailed information about a specific AI model.
    
    Args:
        model_id: Model identifier (e.g., gpt-4, gpt-3.5-turbo)
    
    Returns:
        Model information including capabilities and limits
    """
    try:
        model_info = multimodal_processor.get_model_info(model_id)
        return model_info
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.exception(f"Error getting model info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get model information"
        )

@app.post("/ai/vision")
async def analyze_image(request: VisionRequest):
    """
    Analyze images using vision models.
    
    This endpoint uses GPT-4 Vision or other vision-capable models
    to understand and describe images based on the provided prompt.
    
    Args:
        request: Vision analysis request with prompt and image URL
    
    Returns:
        Image analysis result
    """
    try:
        if not request.prompt or not request.prompt.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prompt cannot be empty"
            )
        
        if not request.image_url or not request.image_url.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Image URL cannot be empty"
            )
        
        result = multimodal_processor.process_vision(
            prompt=request.prompt,
            image_url=request.image_url,
            model_id=request.model,
            max_tokens=request.max_tokens
        )
        
        return {
            "success": True,
            "result": result,
            "model": request.model
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error in vision processing: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process image"
        )

@app.post("/ai/audio/transcribe")
async def transcribe_audio(request: AudioRequest):
    """
    Transcribe audio using Whisper or other audio models.
    
    This endpoint processes audio files and returns text transcription.
    Supports multiple languages and audio formats.
    
    Args:
        request: Audio transcription request with audio URL
    
    Returns:
        Audio transcription result
    """
    try:
        if not request.audio_url or not request.audio_url.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Audio URL cannot be empty"
            )
        
        result = multimodal_processor.process_audio(
            audio_url=request.audio_url,
            model_id=request.model,
            language=request.language
        )
        
        return {
            "success": True,
            "result": result,
            "model": request.model
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error in audio transcription: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to transcribe audio"
        )

@app.post("/ai/fine-tuning/configure")
async def configure_fine_tuning(request: FineTuningRequest):
    """
    Configure fine-tuning for supported models.
    
    This endpoint sets up fine-tuning configuration for models
    that support custom training on your data.
    
    Args:
        request: Fine-tuning configuration request
    
    Returns:
        Fine-tuning configuration status
    """
    try:
        config = FineTuningConfig(
            model_id=request.model,
            training_file=request.training_file,
            validation_file=request.validation_file,
            n_epochs=request.n_epochs or 3,
            batch_size=request.batch_size,
            learning_rate_multiplier=request.learning_rate_multiplier,
            suffix=request.suffix
        )
        
        # Validate configuration
        is_valid, error_message = config.validate()
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
        
        # Check if model supports fine-tuning
        model_info = multimodal_processor.get_model_info(request.model)
        if not model_info.get("supports_fine_tuning"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Model {request.model} does not support fine-tuning"
            )
        
        return {
            "success": True,
            "message": "Fine-tuning configuration validated",
            "config": config.to_dict()
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error configuring fine-tuning: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to configure fine-tuning"
        )

@app.get("/ai/models/fine-tunable")
async def list_fine_tunable_models():
    """
    List all models that support fine-tuning.
    
    Returns:
        List of models that can be fine-tuned
    """
    try:
        models = model_registry.list_models(supports_fine_tuning=True)
        return {
            "models": models,
            "count": len(models)
        }
    except Exception as e:
        logger.exception(f"Error listing fine-tunable models: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list fine-tunable models"
        )


# ============================================================================
# Advanced AI Tools Endpoints
# ============================================================================

class SummarizeRequest(BaseModel):
    """Request model for text summarization"""
    text: str
    max_length: Optional[int] = 128
    style: Optional[str] = "concise"  # concise, detailed, bullet_points

class SentimentRequest(BaseModel):
    """Request model for sentiment analysis"""
    text: str
    detailed: Optional[bool] = False

class EmailDraftRequest(BaseModel):
    """Request model for email drafting"""
    purpose: str
    recipient: Optional[str] = None
    tone: Optional[str] = "professional"
    key_points: Optional[List[str]] = None
    length: Optional[str] = "medium"
    context: Optional[str] = None

class WorkflowRequest(BaseModel):
    """Request model for workflow suggestions"""
    task_description: str
    constraints: Optional[List[str]] = None
    tools_available: Optional[List[str]] = None

@app.post("/ai/tools/summarize")
async def summarize_text(request: SummarizeRequest):
    """
    Summarize text using AI.
    
    This endpoint uses AI to create concise summaries of longer texts.
    Supports different summarization styles and length controls.
    
    Args:
        request: Summarization request with text and options
    
    Returns:
        Text summary with metadata
    """
    try:
        if not request.text or not request.text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text cannot be empty"
            )
        
        if request.max_length < 10 or request.max_length > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="max_length must be between 10 and 1000"
            )
        
        if request.style not in ["concise", "detailed", "bullet_points"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="style must be one of: concise, detailed, bullet_points"
            )
        
        result = summarizer.summarize(
            text=request.text,
            max_length=request.max_length,
            style=request.style
        )
        
        if result.get("status") == "error":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Summarization failed")
            )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error in text summarization: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to summarize text"
        )

@app.post("/ai/tools/sentiment")
async def analyze_sentiment(request: SentimentRequest):
    """
    Analyze sentiment of text.
    
    This endpoint analyzes text to determine sentiment (positive, negative, neutral)
    and can provide detailed emotional analysis.
    
    Args:
        request: Sentiment analysis request
    
    Returns:
        Sentiment analysis results with scores and emotions
    """
    try:
        if not request.text or not request.text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text cannot be empty"
            )
        
        result = sentiment_analyzer.analyze_sentiment(
            text=request.text,
            detailed=request.detailed
        )
        
        if result.get("status") == "error":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Sentiment analysis failed")
            )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error in sentiment analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze sentiment"
        )

@app.post("/ai/tools/email/draft")
async def draft_email(request: EmailDraftRequest):
    """
    Generate an email draft using AI.
    
    This endpoint creates professional email drafts based on purpose,
    tone, and key points. Useful for quick email composition.
    
    Args:
        request: Email drafting request
    
    Returns:
        Email draft with subject and body
    """
    try:
        if not request.purpose or not request.purpose.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email purpose cannot be empty"
            )
        
        if request.tone not in ["professional", "casual", "friendly", "formal"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="tone must be one of: professional, casual, friendly, formal"
            )
        
        if request.length not in ["short", "medium", "long"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="length must be one of: short, medium, long"
            )
        
        result = email_drafter.draft_email(
            purpose=request.purpose,
            recipient=request.recipient,
            tone=request.tone,
            key_points=request.key_points,
            length=request.length,
            context=request.context
        )
        
        if result.get("status") == "error":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Email drafting failed")
            )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error in email drafting: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to draft email"
        )

@app.post("/ai/tools/workflow/suggest")
async def suggest_workflow(request: WorkflowRequest):
    """
    Get AI-suggested workflow for a task.
    
    This endpoint analyzes a task description and suggests an optimal
    workflow with steps, considering constraints and available tools.
    
    Args:
        request: Workflow suggestion request
    
    Returns:
        Suggested workflow with steps and details
    """
    try:
        if not request.task_description or not request.task_description.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task description cannot be empty"
            )
        
        result = workflow_automation.suggest_workflow(
            task_description=request.task_description,
            constraints=request.constraints,
            tools_available=request.tools_available
        )
        
        if result.get("status") == "error":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Workflow suggestion failed")
            )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error in workflow suggestion: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to suggest workflow"
        )

@app.get("/ai/tools")
async def list_ai_tools():
    """
    List all available AI tools and their capabilities.
    
    Returns:
        List of available AI tools with descriptions
    """
    return {
        "tools": [
            {
                "name": "summarize",
                "endpoint": "/ai/tools/summarize",
                "description": "Summarize text with configurable length and style",
                "capabilities": ["concise summary", "detailed summary", "bullet points"]
            },
            {
                "name": "sentiment",
                "endpoint": "/ai/tools/sentiment",
                "description": "Analyze sentiment and emotions in text",
                "capabilities": ["sentiment detection", "emotion analysis", "tone identification"]
            },
            {
                "name": "email_draft",
                "endpoint": "/ai/tools/email/draft",
                "description": "Generate professional email drafts",
                "capabilities": ["email composition", "tone adjustment", "multi-style support"]
            },
            {
                "name": "workflow",
                "endpoint": "/ai/tools/workflow/suggest",
                "description": "Suggest optimal workflows for tasks",
                "capabilities": ["workflow planning", "task optimization", "automation suggestions"]
            }
        ],
        "count": 4
    }
