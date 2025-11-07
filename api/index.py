from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from openai import OpenAI
import os
import asyncio
import logging
from typing import Optional

app = FastAPI()
logger = logging.getLogger("api")
logging.basicConfig(level=logging.INFO)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    # Fail fast during import/startup so misconfiguration is obvious
    logger.error("OPENAI_API_KEY is not set. Set the environment variable and restart the app.")
    raise RuntimeError("OPENAI_API_KEY environment variable is required")

# Read configurable defaults from env
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
try:
    DEFAULT_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
except ValueError:
    logger.error("OPENAI_MAX_TOKENS must be a valid integer. Using default: 1000")
    DEFAULT_MAX_TOKENS = 1000

try:
    DEFAULT_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
except ValueError:
    logger.error("OPENAI_TEMPERATURE must be a valid float. Using default: 0.7")
    DEFAULT_TEMPERATURE = 0.7

# Create client once
client = OpenAI(api_key=OPENAI_API_KEY)


class ChatRequest(BaseModel):
    prompt: str
    # Optional per-request overrides (validated server-side)
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    model: Optional[str] = None


@app.post("/ai/chat")
async def chat_endpoint(request: ChatRequest):
    prompt = request.prompt or ""
    if not prompt.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Prompt cannot be empty")

    # Apply config and clamp values
    max_tokens = request.max_tokens or DEFAULT_MAX_TOKENS
    # Safety: prevent extremely large token requests
    if max_tokens <= 0 or max_tokens > 2000:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="max_tokens must be between 1 and 2000")

    temperature = request.temperature if request.temperature is not None else DEFAULT_TEMPERATURE
    # Validate temperature bounds
    if temperature < 0.0 or temperature > 2.0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="temperature must be between 0.0 and 2.0")

    model = request.model or DEFAULT_MODEL

    try:
        # The OpenAI client call may be blocking — run it in a thread to avoid blocking the event loop
        def call_openai():
            return client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant providing conversational recommendations."},
                    {"role": "user", "content": prompt}
                ],
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
        message = first_choice.get("message") if isinstance(first_choice, dict) else getattr(first_choice, "message", None)
        content = None
        if isinstance(message, dict):
            content = message.get("content")
        elif message is not None:
            # Some SDK responses expose .content
            content = getattr(message, "content", None)

        if not content:
            # Fallback: some older SDKs put text in first_choice.text
            content = first_choice.get("text") if isinstance(first_choice, dict) else getattr(first_choice, "text", None)

        if not content:
            logger.error("Could not parse AI response: %s", response)
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Unexpected AI response format")

        ai_response = content.strip()
        return {"response": ai_response}

    except HTTPException:
        # Re-raise HTTPExceptions raised above
        raise
    except Exception as e:
        # Log the error for debugging, but don't leak internal details to clients
        logger.exception("Error calling OpenAI: %s", e)
        # Map to a 503 to indicate an upstream service problem
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="AI temporarily unavailable")


@app.get("/")
async def root():
    return {"message": "Savrli AI Chat API is running!"}
