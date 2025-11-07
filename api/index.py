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
except ValueError as e:
    logger.error("Invalid OPENAI_MAX_TOKENS value: %s", os.getenv("OPENAI_MAX_TOKENS"))
    raise RuntimeError("OPENAI_MAX_TOKENS must be a valid integer") from e

try:
    DEFAULT_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
except ValueError as e:
    logger.error("Invalid OPENAI_TEMPERATURE value: %s", os.getenv("OPENAI_TEMPERATURE"))
    raise RuntimeError("OPENAI_TEMPERATURE must be a valid float") from e

# Constants for validation
MAX_TOKENS_LIMIT = 2000

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
    if not request.prompt.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Prompt cannot be empty")

    # Apply config and clamp values
    max_tokens = request.max_tokens if request.max_tokens is not None else DEFAULT_MAX_TOKENS
    # Safety: prevent extremely large token requests
    if max_tokens <= 0 or max_tokens > MAX_TOKENS_LIMIT:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"max_tokens must be between 1 and {MAX_TOKENS_LIMIT}")

    temperature = request.temperature if request.temperature is not None else DEFAULT_TEMPERATURE
    # Validate temperature bounds (OpenAI accepts 0.0 to 2.0)
    if temperature < 0.0 or temperature > 2.0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="temperature must be between 0.0 and 2.0")
    
    model = request.model if request.model is not None else DEFAULT_MODEL

    try:
        # Run the OpenAI client call in a thread to avoid blocking the event loop
        response = await asyncio.to_thread(
            lambda: client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant providing conversational recommendations."},
                    {"role": "user", "content": request.prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
        )

        # Defensive parsing
        if not response.choices or len(response.choices) == 0:
            logger.error("OpenAI returned no choices: %s", response)
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="AI returned an empty response")

        # Extract message content from the response
        # Using getattr for defensive access in case of API changes or edge cases
        message = response.choices[0].message
        content = getattr(message, "content", None)

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
