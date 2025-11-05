from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

try:
    from openai import OpenAI  # OpenAI Python SDK v1+
except Exception:
    OpenAI = None  # Will error gracefully at runtime

app = FastAPI(title="Savrli AI Chat Endpoint")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"message": "Savrli AI is running!"}

# Avoid 500s from the browser auto-requesting the favicon
@app.get("/favicon.ico")
def favicon():
    return {}

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not configured")
    if OpenAI is None:
        raise HTTPException(status_code=500, detail="OpenAI SDK is not installed")
    return OpenAI(api_key=api_key)

@app.post("/ai/chat")
async def chat_endpoint(request: ChatRequest):
    prompt = (request.prompt or "").strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
    try:
        client = get_client()
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Savrli's helpful dining assistant named Kai."},
                {"role": "user", "content": prompt},
            ],
        )
        return {"response": resp.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation error: {str(e)}")
