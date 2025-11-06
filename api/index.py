from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

from collections import defaultdict, deque
import uuid
import json
from typing import List

app = FastAPI(title="Savrli AI Chat Endpoint")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

CHAT_HISTORY = defaultdict(lambda: deque(maxlen=10))  # last 10 messages (5 user + 5 AI)

class ChatRequest(BaseModel):
    prompt: str

@app.post("/ai/chat")
async def chat_endpoint(request: ChatRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant providing conversational recommendations."},
                {"role": "user", "content": request.prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        ai_response = response.choices[0].message.content.strip()
        return {"response": ai_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI temporarily unavailable")

@app.get("/")
async def root():
    return {"message": "Savrli AI Chat API is running!"}
