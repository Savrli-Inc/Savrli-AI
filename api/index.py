from fastapi import FastAPI, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI
import os
import asyncio
import logging
import json
from typing import Optional, List, Dict
from datetime import datetime
from collections import defaultdict

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
    # Session management for conversation history
    session_id: Optional[str] = None
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
    
    model = request.model if request.model is not None else DEFAULT_MODEL
    session_id = request.session_id if request.session_id else None  # None if not provided
    
    # Build messages array with conversation history
    messages = [{"role": "system", "content": "You are a helpful assistant providing conversational recommendations."}]
    
    # Add conversation history if session_id is provided
    if session_id in conversation_history:
        # Add recent history (limit to avoid token overflow)
        recent_history = conversation_history[session_id][-10:]  # Last 10 messages
        messages.extend([{"role": msg["role"], "content": msg["content"]} for msg in recent_history])
    
    # Add current user message
    messages.append({"role": "user", "content": request.prompt})
    
    # Store user message in history (only if session_id provided)
    if session_id:
        conversation_history[session_id].append({
            "role": "user",
            "content": request.prompt,
            "timestamp": datetime.utcnow().isoformat()
        })
        trim_conversation_history(session_id)

    try:
        # Handle streaming vs non-streaming responses
        if request.stream:
            return StreamingResponse(
                stream_openai_response(model, messages, max_tokens, temperature, session_id),
                media_type="text/event-stream"
            )
        else:
            # Non-streaming response (original behavior with history support)
            return await get_complete_response(model, messages, max_tokens, temperature, session_id)

    except HTTPException:
        # Re-raise HTTPExceptions raised above
        raise
    except Exception as e:
        # Log the error for debugging, but don't leak internal details to clients
        logger.exception("Error calling OpenAI: %s", e)
        # Map to a 503 to indicate an upstream service problem
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="AI temporarily unavailable")

async def get_complete_response(model: str, messages: List[Dict], max_tokens: int, temperature: float, session_id: str):
    """Get complete non-streaming response"""
    def call_openai():
        return client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )

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
            "timestamp": datetime.utcnow().isoformat()
        })
        trim_conversation_history(session_id)
    
    return {"response": ai_response, "session_id": session_id}

async def stream_openai_response(model: str, messages: List[Dict], max_tokens: int, temperature: float, session_id: str):
    """Stream OpenAI response using Server-Sent Events"""
    full_response = ""
    
    try:
        def create_stream():
            return client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=True
            )
        
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
                "timestamp": datetime.utcnow().isoformat()
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
