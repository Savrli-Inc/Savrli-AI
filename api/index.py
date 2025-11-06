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
    prompt = request.prompt.strip()
    if not prompt:
        raise HTTPException(400, "Prompt required")

    session_id = request.model_extra.get("session_id") if request.model_extra else None
    if not session_id:
        session_id = str(uuid.uuid4())

    history: deque = CHAT_HISTORY[session_id]
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are Savrli AI — the ultimate local vibe expert. "
                "Speak like a cool friend who knows every hidden gem. "
                "Use emojis. Be concise. Never say 'as an AI'. "
                "Focus on: vibe, food, music, crowd, price, and real-time energy."
            )
        }
    ]
    messages.extend(history)
    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=600,
            temperature=0.85,
            tools=[{
                "type": "function",
                "function": {
                    "name": "get_restaurant_vibe",
                    "description": "Look up real-time vibe of a restaurant",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "city": {"type": "string"}
                        },
                        "required": ["name"]
                    }
                }
            }]
        )

        msg = response.choices[0].message
        if msg.tool_calls:
            tool_call = msg.tool_calls[0]
            if tool_call.function.name == "get_restaurant_vibe":
                args = json.loads(tool_call.function.arguments)
                vibe_data = mock_restaurant_lookup(args["name"], args.get("city"))
                messages.append(msg)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": json.dumps(vibe_data)
                })
                second = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=600
                )
                ai_text = second.choices[0].message.content.strip()
            else:
                ai_text = msg.content.strip()
        else:
            ai_text = msg.content.strip()

        history.append({"role": "user", "content": prompt})
        history.append({"role": "assistant", "content": ai_text})

        return {"response": ai_text, "session_id": session_id}

    except Exception as e:
        raise HTTPException(500, "AI unavailable")
        
