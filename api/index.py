"""
Savrli AI – Full FastAPI Server
Includes:
- Chat with streaming & session history
- /demo page with interactive test harness
- File upload endpoint
- Static file serving
- OpenAI integration
- Environment config
"""
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI
import os
import asyncio
import logging
import json
from typing import Optional, List, Dict
from datetime import datetime, timezone
from collections import defaultdict
from pathlib import Path
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# ----------------------------------------------------------------------
# Load .env
# ----------------------------------------------------------------------
load_dotenv()

# Import resources router
from .resources import router as resources_router

# ----------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------
logger = logging.getLogger("api")
logging.basicConfig(level=logging.INFO)

# ----------------------------------------------------------------------
# OpenAI Client & Config
# ----------------------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    error = """
    OPENAI_API_KEY NOT SET
    1. Copy .env.example to .env
    2. Add: OPENAI_API_KEY=sk-...
    3. Restart server
    """
    logger.error(error)
    raise RuntimeError("OPENAI_API_KEY is required")

client = OpenAI(api_key=OPENAI_API_KEY)

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
DEFAULT_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
DEFAULT_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
DEFAULT_CONTEXT_WINDOW = int(os.getenv("DEFAULT_CONTEXT_WINDOW", "10"))
MAX_HISTORY_PER_SESSION = int(os.getenv("MAX_HISTORY_PER_SESSION", "20"))

# In-memory conversation history
conversation_history: Dict[str, List[Dict]] = defaultdict(list)

# ----------------------------------------------------------------------
# FastAPI App + Lifespan
# ----------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    welcome = f"""
    Savrli AI Server Started!
    • Model: {DEFAULT_MODEL}
    • Playground: http://localhost:8000/playground
    • Demo: http://localhost:8000/demo
    • API Root: http://localhost:8000/
    • Docs: http://localhost:8000/docs
    """
    print(welcome)
    logger.info("Server started")
    yield
    logger.info("Server shutting down")


app = FastAPI(lifespan=lifespan)

# ----------------------------------------------------------------------
# Static files & Routers
# ----------------------------------------------------------------------
static_path = Path(__file__).parent.parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Resources router (for /api/resources/* etc.)
app.include_router(resources_router)

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def trim_history(session_id: str):
    if len(conversation_history[session_id]) > MAX_HISTORY_PER_SESSION:
        conversation_history[session_id] = conversation_history[session_id][-MAX_HISTORY_PER_SESSION:]


# ----------------------------------------------------------------------
# Pydantic Models
# ----------------------------------------------------------------------
class ChatRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    model: Optional[str] = None
    session_id: Optional[str] = None
    stream: Optional[bool] = False


# ----------------------------------------------------------------------
# Routes – Root & Pages
# ----------------------------------------------------------------------
@app.get("/")
async def root():
    return {
        "message": "Savrli AI API is running",
        "endpoints": {
            "playground": "/playground",
            "demo": "/demo",
            "chat": "POST /ai/chat",
            "upload": "POST /api/resources/upload",
            "resources_page": "/resources",
            "health": "/health",
        },
        "docs": "/docs",
    }


@app.get("/playground", response_class=HTMLResponse)
async def playground():
    path = Path(__file__).parent.parent / "pages" / "playground.html"
    return HTMLResponse(path.read_text(encoding="utf-8")) if path.exists() else "Playground not found"


@app.get("/demo", response_class=HTMLResponse)
async def demo():
    """Demo page for manual testing of playground and multimodal endpoints"""
    path = Path(__file__).parent.parent / "pages" / "demo.html"
    return HTMLResponse(path.read_text(encoding="utf-8")) if path.exists() else "Demo page not found"


@app.get("/resources", response_class=HTMLResponse)
async def resources_page():
    """Static page listing uploaded / managed resources (front-end demo)."""
    path = Path(__file__).parent.parent / "pages" / "resources.html"
    return HTMLResponse(path.read_text(encoding="utf-8")) if path.exists() else "Resources page not found"


# ----------------------------------------------------------------------
# Core AI Chat Endpoint
# ----------------------------------------------------------------------
@app.post("/ai/chat")
async def chat_endpoint(request: ChatRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    model = request.model or DEFAULT_MODEL
    max_tokens = request.max_tokens or DEFAULT_MAX_TOKENS
    temp = request.temperature or DEFAULT_TEMPERATURE
    session_id = request.session_id

    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    if session_id and session_id in conversation_history:
        recent = conversation_history[session_id][-DEFAULT_CONTEXT_WINDOW:]
        messages.extend([{"role": m["role"], "content": m["content"]} for m in recent])

    messages.append({"role": "user", "content": request.prompt})

    if session_id:
        conversation_history[session_id].append(
            {
                "role": "user",
                "content": request.prompt,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )
        trim_history(session_id)

    try:
        if request.stream:
            return StreamingResponse(
                stream_response(model, messages, max_tokens, temp, session_id),
                media_type="text/event-stream",
            )
        else:
            resp = await asyncio.to_thread(
                client.chat.completions.create,
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temp,
            )
            content = resp.choices[0].message.content.strip()

            if session_id:
                conversation_history[session_id].append(
                    {
                        "role": "assistant",
                        "content": content,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                )
                trim_history(session_id)

            return {"response": content, "session_id": session_id}
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        raise HTTPException(503, "AI unavailable")


async def stream_response(model, messages, max_tokens, temp, session_id):
    full = ""
    try:
        stream = await asyncio.to_thread(
            client.chat.completions.create,
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temp,
            stream=True,
        )
        for chunk in stream:
            if delta := chunk.choices[0].delta.content:
                full += delta
                yield f"data: {json.dumps({'content': delta})}\n\n"
        yield "data: {\"done\": true}\n\n"

        if session_id:
            conversation_history[session_id].append(
                {
                    "role": "assistant",
                    "content": full,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            )
            trim_history(session_id)
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"


# ----------------------------------------------------------------------
# Demo: File Upload Endpoint
# ----------------------------------------------------------------------
@app.post("/api/resources/upload")
async def upload_resource(file: UploadFile = File(...)):
    """
    Generic resource upload endpoint for testing file uploads.
    Accepts any file and returns metadata about the uploaded file.
    """
    try:
        file_data = await file.read()
        size = len(file_data)
        size_formatted = f"{size / 1024:.2f} KB" if size > 1024 else f"{size} bytes"
        return {
            "success": True,
            "message": "File uploaded successfully",
            "file_info": {
                "filename": file.filename,
                "content_type": file.content_type or "application/octet-stream",
                "size": size,
                "size_formatted": size_formatted,
            },
        }
    except Exception as e:
        logger.exception("Upload error: %s", e)
        raise HTTPException(status_code=500, detail="File upload failed")


# ----------------------------------------------------------------------
# Health Check
# ----------------------------------------------------------------------
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model": DEFAULT_MODEL,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

