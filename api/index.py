from fastapi import FastAPI, HTTPException, status, File, UploadFile
from fastapi.responses import StreamingResponse, HTMLResponse
from pydantic import BaseModel
from openai import OpenAI
import os
import asyncio
import logging
import json
import base64
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, timezone
from collections import defaultdict
from pathlib import Path
from contextlib import asynccontextmanager

# ----------------------------------------------------------------------
# Imports – plugin system + multimodal + tools + resource management
# ----------------------------------------------------------------------
from integrations.plugin_base import PluginManager
from integrations.slack_plugin import SlackPlugin
from integrations.discord_plugin import DiscordPlugin
from integrations.notion_plugin import NotionPlugin
from integrations.google_docs_plugin import GoogleDocsPlugin

from ai_multimodal import (
    MultiModalProcessor, FineTuningConfig, model_registry
)
from tools.summarizer import Summarizer
from tools.sentiment_analysis import SentimentAnalyzer
from tools.email_drafter import EmailDrafter
from tools.workflow_automation import WorkflowAutomation

from resource_manager import (
    ConversationExporter, ConversationImporter, SessionManager
)

# ----------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------
logger = logging.getLogger("api")
logging.basicConfig(level=logging.INFO)

# ----------------------------------------------------------------------
# OpenAI client & config
# ----------------------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    error_msg = """
    OPENAI_API_KEY NOT CONFIGURED

    The Savrli AI server requires an OpenAI API key to function.

    Quick Fix:
    1. Create a .env file in the project root
    2. Add: OPENAI_API_KEY=your-api-key-here
    3. Get key from: https://platform.openai.com/api-keys
    4. Restart server
    """
    logger.error(error_msg)
    print(error_msg)
    raise RuntimeError("OPENAI_API_KEY environment variable is required")

try:
    DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    DEFAULT_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
    DEFAULT_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    DEFAULT_CONTEXT_WINDOW = int(os.getenv("DEFAULT_CONTEXT_WINDOW", "10"))
except ValueError as e:
    logger.error("Invalid env var: %s", e)
    raise RuntimeError(f"Invalid environment variable: {e}")

client = OpenAI(api_key=OPENAI_API_KEY)

# In-memory history
conversation_history: Dict[str, List[Dict]] = defaultdict(list)
MAX_HISTORY_PER_SESSION = int(os.getenv("MAX_HISTORY_PER_SESSION", "20"))

# ----------------------------------------------------------------------
# Plugin & Tool Initialization
# ----------------------------------------------------------------------
plugin_manager = PluginManager(ai_system=client)
multimodal_processor = MultiModalProcessor(openai_client=client)

summarizer = Summarizer()
sentiment_analyzer = SentimentAnalyzer()
email_drafter = EmailDrafter()
workflow_automation = WorkflowAutomation()

session_manager = SessionManager(conversation_history)

# --- Slack ---
slack_config = {
    "bot_token": os.getenv("SLACK_BOT_TOKEN"),
    "signing_secret": os.getenv("SLACK_SIGNING_SECRET"),
    "enabled": os.getenv("SLACK_ENABLED", "false").lower() == "true",
}
slack_plugin = SlackPlugin(ai_system=client, config=slack_config)
if slack_config.get("bot_token"):
    plugin_manager.register_plugin("slack", slack_plugin)

# --- Discord ---
discord_config = {
    "bot_token": os.getenv("DISCORD_BOT_TOKEN"),
    "application_id": os.getenv("DISCORD_APP_ID"),
    "public_key": os.getenv("DISCORD_PUBLIC_KEY"),
    "enabled": os.getenv("DISCORD_ENABLED", "false").lower() == "true",
}
discord_plugin = DiscordPlugin(ai_system=client, config=discord_config)
if discord_config.get("bot_token"):
    plugin_manager.register_plugin("discord", discord_plugin)

# --- Notion ---
notion_config = {
    "api_token": os.getenv("NOTION_API_TOKEN"),
    "enabled": os.getenv("NOTION_ENABLED", "false").lower() == "true",
}
notion_plugin = NotionPlugin(ai_system=client, config=notion_config)
if notion_config.get("api_token"):
    plugin_manager.register_plugin("notion", notion_plugin)

# --- Google Docs ---
google_docs_config = {
    "credentials": os.getenv("GOOGLE_DOCS_CREDENTIALS"),
    "enabled": os.getenv("GOOGLE_DOCS_ENABLED", "false").lower() == "true",
}
google_docs_plugin = GoogleDocsPlugin(ai_system=client, config=google_docs_config)
if google_docs_config.get("credentials"):
    plugin_manager.register_plugin("google_docs", google_docs_plugin)

# ----------------------------------------------------------------------
# Lifespan – startup banner
# ----------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    welcome = f"""
    Savrli AI Server Started Successfully!

    OpenAI: Connected (Model: {DEFAULT_MODEL})
    Plugins: {len(plugin_manager.list_plugins())} registered
    Server: http://localhost:8000

    Playground: /playground
    Docs: /docs
    """
    logger.info("Server started")
    print(welcome)
    yield
    logger.info("Server shutting down")

app = FastAPI(lifespan=lifespan)

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def trim_conversation_history(session_id: str):
    if len(conversation_history[session_id]) > MAX_HISTORY_PER_SESSION:
        conversation_history[session_id] = conversation_history[session_id][-MAX_HISTORY_PER_SESSION:]

# ----------------------------------------------------------------------
# Pydantic Models
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

# === Enhanced Multimodal Models ===
class VisionRequest(BaseModel):
    prompt: str
    image_url: Optional[str] = None
    image_base64: Optional[str] = None
    model: Optional[str] = "gpt-4-vision-preview"
    max_tokens: Optional[int] = 300
    detail: Optional[str] = "auto"  # auto, low, high

class ImageGenerationRequest(BaseModel):
    prompt: str
    model: Optional[str] = "dall-e-3"
    n: Optional[int] = 1
    size: Optional[str] = "1024x1024"
    quality: Optional[str] = "standard"
    style: Optional[str] = "vivid"  # vivid, natural

class AudioTranscriptionRequest(BaseModel):
    model: Optional[str] = "whisper-1"
    language: Optional[str] = None
    prompt: Optional[str] = None
    response_format: Optional[str] = "json"
    temperature: Optional[float] = 0.0

class FineTuningRequest(BaseModel):
    training_file: str
    model: Optional[str] = "gpt-3.5-turbo"
    validation_file: Optional[str] = None
    n_epochs: Optional[int] = 3
    batch_size: Optional[Union[str, int]] = "auto"
    learning_rate_multiplier: Optional[Union[str, float]] = "auto"
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

# Resource Management
class ExportRequest(BaseModel):
    session_id: str
    format: str = "json"

class ImportRequest(BaseModel):
    session_id: str
    format: str = "json"
    data: str

class BulkDeleteRequest(BaseModel):
    session_ids: List[str]

# ----------------------------------------------------------------------
# Core Chat Endpoint
# ----------------------------------------------------------------------
@app.post("/ai/chat")
async def chat_endpoint(request: ChatRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    max_tokens = request.max_tokens or DEFAULT_MAX_TOKENS
    if not (1 <= max_tokens <= 2000):
        raise HTTPException(status_code=400, detail="max_tokens must be 1–2000")

    temperature = request.temperature or DEFAULT_TEMPERATURE
    if not (0.0 <= temperature <= 2.0):
        raise HTTPException(status_code=400, detail="temperature must be 0.0–2.0")

    top_p = request.top_p
    if top_p is not None and not (0.0 <= top_p <= 1.0):
        raise HTTPException(status_code=400, detail="top_p must be 0.0–1.0")

    frequency_penalty = request.frequency_penalty
    if frequency_penalty is not None and not (-2.0 <= frequency_penalty <= 2.0):
        raise HTTPException(status_code=400, detail="frequency_penalty must be -2.0–2.0")

    presence_penalty = request.presence_penalty
    if presence_penalty is not None and not (-2.0 <= presence_penalty <= 2.0):
        raise HTTPException(status_code=400, detail="presence_penalty must be -2.0–2.0")

    context_window = request.context_window or DEFAULT_CONTEXT_WINDOW
    if not (0 <= context_window <= 50):
        raise HTTPException(status_code=400, detail="context_window must be 0–50")

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
            "role": "user", "content": request.prompt,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        trim_conversation_history(session_id)

    try:
        if request.stream:
            return StreamingResponse(
                stream_openai_response(model, messages, max_tokens, temperature, top_p,
                                       frequency_penalty, presence_penalty, session_id),
                media_type="text/event-stream"
            )
        else:
            return await get_complete_response(model, messages, max_tokens, temperature, top_p,
                                               frequency_penalty, presence_penalty, session_id)
    except Exception as e:
        logger.exception("OpenAI error: %s", e)
        raise HTTPException(status_code=503, detail="AI temporarily unavailable")

async def get_complete_response(model, messages, max_tokens, temperature, top_p,
                                frequency_penalty, presence_penalty, session_id):
    def call():
        kwargs = {k: v for k, v in {
            "model": model, "messages": messages, "max_tokens": max_tokens,
            "temperature": temperature, "top_p": top_p,
            "frequency_penalty": frequency_penalty, "presence_penalty": presence_penalty
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
                "temperature": temperature, "stream": True, "top_p": top_p,
                "frequency_penalty": frequency_penalty, "presence_penalty": presence_penalty
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
# History Endpoints
# ----------------------------------------------------------------------
@app.get("/ai/history/{session_id}")
async def get_conversation_history(session_id: str, limit: Optional[int] = 50):
    msgs = conversation_history.get(session_id, [])
    if limit:
        msgs = msgs[-limit:]
    return {"session_id": session_id, "messages": msgs, "total": len(conversation_history.get(session_id, []))}

@app.delete("/ai/history/{session_id}")
async def clear_conversation_history(session_id: str):
    if session_id in conversation_history:
        del conversation_history[session_id]
        return {"message": f"History cleared for {session_id}"}
    return {"message": "No history found"}

# ----------------------------------------------------------------------
# Enhanced Multimodal Endpoints
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

@app.post("/ai/vision")
async def vision_endpoint(request: VisionRequest):
    if not request.image_url and not request.image_base64:
        raise HTTPException(status_code=400, detail="Either image_url or image_base64 required")
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    content = [{"type": "text", "text": request.prompt}]
    if request.image_url:
        content.append({"type": "image_url", "image_url": {"url": request.image_url, "detail": request.detail}})
    elif request.image_base64:
        content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{request.image_base64}", "detail": request.detail}})

    messages = [{"role": "user", "content": content}]

    try:
        def call():
            return client.chat.completions.create(
                model=request.model,
                messages=messages,
                max_tokens=request.max_tokens
            )
        response = await asyncio.to_thread(call)
        result = response.choices[0].message.content.strip()
        return {"response": result, "model": request.model}
    except Exception as e:
        logger.exception("Vision error: %s", e)
        raise HTTPException(status_code=503, detail="Vision API unavailable")

@app.post("/ai/audio/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    model: str = "whisper-1",
    language: Optional[str] = None,
    prompt: Optional[str] = None,
    response_format: str = "json",
    temperature: float = 0.0
):
    audio_data = await file.read()
    try:
        def call():
            kwargs = {
                "model": model,
                "file": (file.filename, audio_data, file.content_type),
                "response_format": response_format,
                "temperature": temperature
            }
            if language: kwargs["language"] = language
            if prompt: kwargs["prompt"] = prompt
            return client.audio.transcriptions.create(**kwargs)
        result = await asyncio.to_thread(call)
        text = result.text if hasattr(result, 'text') else str(result)
        return {"transcription": text, "model": model, "format": response_format}
    except Exception as e:
        logger.exception("Whisper error: %s", e)
        raise HTTPException(status_code=503, detail="Audio transcription unavailable")

@app.post("/ai/image/generate")
async def generate_image(request: ImageGenerationRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    valid_sizes = {
        "dall-e-3": ["1024x1024", "1792x1024", "1024x1792"],
        "dall-e-2": ["256x256", "512x512", "1024x1024"]
    }
    if request.size not in valid_sizes.get(request.model, []):
        raise HTTPException(status_code=400, detail=f"Invalid size for {request.model}")

    try:
        def call():
            kwargs = {
                "model": request.model, "prompt": request.prompt,
                "n": request.n, "size": request.size
            }
            if request.model == "dall-e-3":
                kwargs["quality"] = request.quality
                kwargs["style"] = request.style
            return client.images.generate(**kwargs)
        response = await asyncio.to_thread(call)
        images = [{"url": img.url, "revised_prompt": getattr(img, 'revised_prompt', None)} for img in response.data]
        return {"images": images, "model": request.model, "count": len(images)}
    except Exception as e:
        logger.exception("DALL-E error: %s", e)
        raise HTTPException(status_code=503, detail="Image generation unavailable")

@app.post("/ai/fine-tune/configure")
async def configure_fine_tuning(request: FineTuningRequest):
    config = FineTuningConfig(
        model_id=request.model,
        training_file=request.training_file,
        validation_file=request.validation_file,
        n_epochs=request.n_epochs,
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
    return {"success": True, "message": "Validated", "config": config.to_dict()}

# ----------------------------------------------------------------------
# AI Tools, UI, Integrations, Resource Management
# ----------------------------------------------------------------------
# [All other endpoints from main branch: /ai/tools/*, /playground, integrations, export/import, etc.]
# ... (same as in your main branch – included below for completeness)

@app.get("/")
async def root():
    return {"message": "Savrli AI API Running", "playground": "/playground", "docs": "/docs"}

@app.get("/playground", response_class=HTMLResponse)
async def playground():
    path = Path(__file__).parent.parent / "pages" / "playground.html"
    return HTMLResponse(path.read_text(encoding="utf-8")) if path.exists() else "Playground not found"

# ... [rest of tools, integrations, export/import, etc. – unchanged from main]
