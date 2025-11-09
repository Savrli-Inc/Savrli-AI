from fastapi import FastAPI, HTTPException, status, File, UploadFile
from fastapi.responses import StreamingResponse, HTMLResponse, FileResponse
from pydantic import BaseModel
from openai import OpenAI
import os
import asyncio
import logging
import json
import base64
from typing import Optional, List, Dict, Union
from datetime import datetime, timezone
from collections import defaultdict
from pathlib import Path
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from ai_capabilities import AICapability, FineTuningConfig, SupportedModel

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

class VisionRequest(BaseModel):
    """Request model for image analysis using vision models"""
    prompt: str
    image_url: Optional[str] = None
    image_base64: Optional[str] = None
    model: Optional[str] = "gpt-4-vision-preview"
    max_tokens: Optional[int] = 300
    detail: Optional[str] = "auto"  # "auto", "low", or "high"

class AudioTranscriptionRequest(BaseModel):
    """Request model for audio transcription"""
    model: Optional[str] = "whisper-1"
    language: Optional[str] = None
    prompt: Optional[str] = None
    response_format: Optional[str] = "json"  # json, text, srt, verbose_json, or vtt
    temperature: Optional[float] = 0.0

class ImageGenerationRequest(BaseModel):
    """Request model for image generation"""
    prompt: str
    model: Optional[str] = "dall-e-3"
    n: Optional[int] = 1
    size: Optional[str] = "1024x1024"  # dall-e-3: 1024x1024, 1792x1024, 1024x1792
    quality: Optional[str] = "standard"  # standard or hd
    style: Optional[str] = "vivid"  # vivid or natural

class FineTuningRequest(BaseModel):
    """Request model for fine-tuning configuration"""
    training_file: str
    model: Optional[str] = "gpt-3.5-turbo"
    validation_file: Optional[str] = None
    n_epochs: Optional[int] = 3
    batch_size: Optional[str] = "auto"
    learning_rate_multiplier: Optional[str] = "auto"
    suffix: Optional[str] = None

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

@app.post("/ai/vision")
async def vision_endpoint(request: VisionRequest):
    """
    Analyze images using GPT-4 Vision or similar models
    
    Accepts either an image URL or base64-encoded image data.
    """
    if not request.image_url and not request.image_base64:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either image_url or image_base64 must be provided"
        )
    
    if not request.prompt.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prompt cannot be empty"
        )
    
    try:
        # Build the message content
        content = [
            {"type": "text", "text": request.prompt}
        ]
        
        if request.image_url:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": request.image_url,
                    "detail": request.detail
                }
            })
        elif request.image_base64:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{request.image_base64}",
                    "detail": request.detail
                }
            })
        
        messages = [
            {
                "role": "user",
                "content": content
            }
        ]
        
        def call_openai():
            return client.chat.completions.create(
                model=request.model,
                messages=messages,
                max_tokens=request.max_tokens
            )
        
        response = await asyncio.to_thread(call_openai)
        
        # Extract response
        if not response.choices or len(response.choices) == 0:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI returned an empty response"
            )
        
        content = response.choices[0].message.content
        
        return {
            "response": content,
            "model": request.model,
            "input_type": "image"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error calling OpenAI Vision API: %s", e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Vision API temporarily unavailable"
        )

@app.post("/ai/audio/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    model: str = "whisper-1",
    language: Optional[str] = None,
    prompt: Optional[str] = None,
    response_format: str = "json",
    temperature: float = 0.0
):
    """
    Transcribe audio using Whisper API
    
    Accepts audio file upload and returns transcription.
    """
    try:
        # Read the uploaded file
        audio_data = await file.read()
        
        # Create a temporary file to pass to OpenAI
        # OpenAI API requires a file object
        def call_openai():
            # Create kwargs with only non-None parameters
            kwargs = {
                "model": model,
                "file": (file.filename, audio_data, file.content_type)
            }
            if language:
                kwargs["language"] = language
            if prompt:
                kwargs["prompt"] = prompt
            if response_format:
                kwargs["response_format"] = response_format
            if temperature != 0.0:
                kwargs["temperature"] = temperature
            
            return client.audio.transcriptions.create(**kwargs)
        
        result = await asyncio.to_thread(call_openai)
        
        # Handle different response formats
        if response_format == "json" or response_format == "verbose_json":
            return {
                "transcription": result.text if hasattr(result, 'text') else str(result),
                "model": model,
                "input_type": "audio"
            }
        else:
            # For text, srt, vtt formats, return as plain text
            return {
                "transcription": str(result),
                "model": model,
                "input_type": "audio",
                "format": response_format
            }
        
    except Exception as e:
        logger.exception("Error calling Whisper API: %s", e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Audio transcription temporarily unavailable"
        )

@app.post("/ai/image/generate")
async def generate_image(request: ImageGenerationRequest):
    """
    Generate images using DALL-E models
    
    Creates images from text prompts.
    """
    if not request.prompt.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prompt cannot be empty"
        )
    
    # Validate size based on model
    valid_sizes = {
        "dall-e-3": ["1024x1024", "1792x1024", "1024x1792"],
        "dall-e-2": ["256x256", "512x512", "1024x1024"]
    }
    
    if request.size not in valid_sizes.get(request.model, []):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid size for {request.model}. Valid sizes: {', '.join(valid_sizes.get(request.model, []))}"
        )
    
    try:
        def call_openai():
            kwargs = {
                "model": request.model,
                "prompt": request.prompt,
                "n": request.n,
                "size": request.size
            }
            
            # DALL-E 3 specific parameters
            if request.model == "dall-e-3":
                kwargs["quality"] = request.quality
                kwargs["style"] = request.style
            
            return client.images.generate(**kwargs)
        
        response = await asyncio.to_thread(call_openai)
        
        # Extract image URLs
        images = [
            {
                "url": image.url,
                "revised_prompt": getattr(image, 'revised_prompt', None)
            }
            for image in response.data
        ]
        
        return {
            "images": images,
            "model": request.model,
            "count": len(images)
        }
        
    except Exception as e:
        logger.exception("Error calling DALL-E API: %s", e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Image generation temporarily unavailable"
        )

@app.get("/ai/models")
async def list_models():
    """
    List all supported AI models and their capabilities
    
    Returns information about available models for text, image, and audio processing.
    """
    capability = AICapability("default", ["text", "image", "audio"])
    models_info = capability.get_model_info()
    
    return {
        "models": models_info["supported_models"],
        "total_count": models_info["total_count"],
        "capabilities": {
            "text": ["gpt-4", "gpt-4-turbo-preview", "gpt-3.5-turbo"],
            "image_analysis": ["gpt-4-vision-preview"],
            "image_generation": ["dall-e-3", "dall-e-2"],
            "audio": ["whisper-1", "tts-1", "tts-1-hd"]
        }
    }

@app.get("/ai/models/{model_name}")
async def get_model_info(model_name: str):
    """
    Get detailed information about a specific model
    
    Returns capabilities and configuration options for the specified model.
    """
    capability = AICapability("default", ["text", "image", "audio"])
    model_info = capability.get_model_info(model_name)
    
    if model_info.get("status") == "not_found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model {model_name} not found"
        )
    
    return model_info

@app.post("/ai/fine-tune/configure")
async def configure_fine_tuning(request: FineTuningRequest):
    """
    Configure fine-tuning for AI models
    
    Sets up fine-tuning configuration with training dataset and hyperparameters.
    Note: This endpoint configures fine-tuning parameters. 
    Actual fine-tuning requires OpenAI API fine-tuning jobs.
    """
    try:
        config = FineTuningConfig(
            training_file=request.training_file,
            model=request.model,
            validation_file=request.validation_file,
            hyperparameters={
                "n_epochs": request.n_epochs,
                "batch_size": request.batch_size,
                "learning_rate_multiplier": request.learning_rate_multiplier
            },
            suffix=request.suffix
        )
        
        capability = AICapability(request.model, ["text"])
        result = capability.fine_tune(config)
        
        return {
            "configuration": config.to_dict(),
            "status": result["status"],
            "message": result["message"],
            "note": "Use OpenAI's fine-tuning API to start the actual fine-tuning job with this configuration"
        }
        
    except Exception as e:
        logger.exception("Error configuring fine-tuning: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error configuring fine-tuning: {str(e)}"
        )

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
