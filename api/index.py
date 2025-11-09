from fastapi import FastAPI, HTTPException, status
from fastapi.responses import StreamingResponse, HTMLResponse, FileResponse
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

class SummarizeRequest(BaseModel):
    text: str
    max_length: Optional[int] = None  # Maximum length of summary in words
    model: Optional[str] = None

class SentimentRequest(BaseModel):
    text: str
    model: Optional[str] = None

class EmailDraftRequest(BaseModel):
    context: str  # What the email is about
    recipient: Optional[str] = None  # Who the email is to
    tone: Optional[str] = "professional"  # professional, casual, formal, friendly
    purpose: Optional[str] = None  # request, response, update, etc.
    model: Optional[str] = None

@app.post("/ai/summarize")
async def summarize_endpoint(request: SummarizeRequest):
    """
    Summarize text using AI
    
    This endpoint takes a longer text and returns a concise summary.
    Useful for condensing articles, documents, or long messages.
    """
    if not request.text.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Text cannot be empty")
    
    model = request.model if request.model is not None else DEFAULT_MODEL
    
    # Build the prompt for summarization
    max_length_instruction = ""
    if request.max_length:
        max_length_instruction = f" in approximately {request.max_length} words"
    
    system_message = f"You are a professional text summarizer. Provide clear, concise summaries{max_length_instruction}."
    user_message = f"Please summarize the following text:\n\n{request.text}"
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    try:
        def call_openai():
            return client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=500,
                temperature=0.5  # Lower temperature for more focused summaries
            )
        
        response = await asyncio.to_thread(call_openai)
        
        choices = getattr(response, "choices", None)
        if not choices or len(choices) == 0:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="AI returned an empty response")
        
        message = choices[0].message if hasattr(choices[0], 'message') else choices[0].get("message")
        content = message.content if hasattr(message, 'content') else message.get("content")
        
        if not content:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Unexpected AI response format")
        
        summary = content.strip()
        
        return {
            "summary": summary,
            "original_length": len(request.text.split()),
            "summary_length": len(summary.split())
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error calling OpenAI for summarization: %s", e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="AI temporarily unavailable")

@app.post("/ai/sentiment")
async def sentiment_endpoint(request: SentimentRequest):
    """
    Analyze sentiment of text using AI
    
    This endpoint analyzes the emotional tone and sentiment of the provided text,
    returning a sentiment label (positive, negative, neutral) and confidence score.
    """
    if not request.text.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Text cannot be empty")
    
    model = request.model if request.model is not None else DEFAULT_MODEL
    
    system_message = """You are a sentiment analysis expert. Analyze the sentiment of the given text and respond ONLY with a JSON object in this exact format:
{"sentiment": "positive" or "negative" or "neutral", "confidence": 0.0-1.0, "reasoning": "brief explanation"}"""
    
    user_message = f"Analyze the sentiment of this text:\n\n{request.text}"
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    try:
        def call_openai():
            return client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=200,
                temperature=0.3  # Lower temperature for more consistent analysis
            )
        
        response = await asyncio.to_thread(call_openai)
        
        choices = getattr(response, "choices", None)
        if not choices or len(choices) == 0:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="AI returned an empty response")
        
        message = choices[0].message if hasattr(choices[0], 'message') else choices[0].get("message")
        content = message.content if hasattr(message, 'content') else message.get("content")
        
        if not content:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Unexpected AI response format")
        
        # Parse JSON response
        try:
            result = json.loads(content.strip())
            return {
                "sentiment": result.get("sentiment", "neutral"),
                "confidence": result.get("confidence", 0.5),
                "reasoning": result.get("reasoning", "")
            }
        except json.JSONDecodeError:
            # Fallback if AI doesn't return valid JSON
            logger.warning("AI did not return valid JSON for sentiment analysis")
            return {
                "sentiment": "neutral",
                "confidence": 0.5,
                "reasoning": content.strip()
            }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error calling OpenAI for sentiment analysis: %s", e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="AI temporarily unavailable")

@app.post("/ai/draft-email")
async def draft_email_endpoint(request: EmailDraftRequest):
    """
    Generate email drafts using AI
    
    This endpoint creates professional email drafts based on the provided context.
    Supports different tones (professional, casual, formal, friendly) and purposes.
    """
    if not request.context.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Context cannot be empty")
    
    # Validate tone
    valid_tones = ["professional", "casual", "formal", "friendly"]
    tone = request.tone.lower() if request.tone else "professional"
    if tone not in valid_tones:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Tone must be one of: {', '.join(valid_tones)}"
        )
    
    model = request.model if request.model is not None else DEFAULT_MODEL
    
    # Build the prompt for email drafting
    recipient_part = f" to {request.recipient}" if request.recipient else ""
    purpose_part = f"Purpose: {request.purpose}\n" if request.purpose else ""
    
    system_message = f"""You are a professional email writer. Draft clear, well-structured emails with a {tone} tone. 
Include a subject line, greeting, body, and closing. Format the email properly."""
    
    user_message = f"""Draft an email{recipient_part} with the following context:

{purpose_part}Context: {request.context}

Please provide:
1. Subject line
2. Complete email body with greeting and closing"""
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    try:
        def call_openai():
            return client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=800,
                temperature=0.7
            )
        
        response = await asyncio.to_thread(call_openai)
        
        choices = getattr(response, "choices", None)
        if not choices or len(choices) == 0:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="AI returned an empty response")
        
        message = choices[0].message if hasattr(choices[0], 'message') else choices[0].get("message")
        content = message.content if hasattr(message, 'content') else message.get("content")
        
        if not content:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Unexpected AI response format")
        
        email_draft = content.strip()
        
        return {
            "email_draft": email_draft,
            "tone": tone,
            "recipient": request.recipient
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error calling OpenAI for email drafting: %s", e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="AI temporarily unavailable")

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
