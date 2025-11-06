from fastapi import FastAPI, HTTPException, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from collections import defaultdict, deque
import uuid
import json

app = FastAPI(title="Savrli AI Chat Endpoint")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Memory: keeps last 10 messages per session (5 user + 5 AI)
CHAT_HISTORY = defaultdict(lambda: deque(maxlen=10))

class ChatRequest(BaseModel):
    prompt: str
    model_extra: dict | None = None  # used to pass session_id from frontend

@app.post("/ai/chat")
async def chat_endpoint(request: ChatRequest):
    prompt = request.prompt.strip()
    if not prompt:
        raise HTTPException(400, "Prompt required")

    # Get or create session
    session_id = request.model_extra.get("session_id") if request.model_extra else None
    if not session_id:
        session_id = str(uuid.uuid4())

    history: deque = CHAT_HISTORY[session_id]

    # Build message list with system prompt + history + new user message
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

        # Handle tool call (mock restaurant lookup)
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

        # Save to memory
        history.append({"role": "user", "content": prompt})
        history.append({"role": "assistant", "content": ai_text})

        return {"response": ai_text, "session_id": session_id}

    except Exception as e:
        raise HTTPException(500, "AI unavailable")


@app.get("/ai/chat", response_class=HTMLResponse)
async def chat_ui():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Savrli AI</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 0; background: #0f0f0f; color: #fff; }
    #chat { max-width: 600px; margin: 0 auto; padding: 1rem; }
    .msg { margin: 0.5rem 0; padding: 0.75rem 1rem; border-radius: 12px; max-width: 80%; }
    .user { background: #4a90e2; align-self: flex-end; margin-left: auto; }
    .ai { background: #333; align-self: flex-start; }
    .typing { opacity: 0.7; font-style: italic; }
    #input-area { display: flex; gap: 0.5rem; margin-top: 1rem; }
    input { flex: 1; padding: 0.75rem; border: 1px solid #444; border-radius: 8px; background: #222; color: #fff; }
    button { padding: 0.75rem 1.5rem; background: #4a90e2; color: white; border: none; border-radius: 8px; cursor: pointer; }
    button:hover { background: #357abd; }
  </style>
</head>
<body>
  <div id="chat">
    <div id="messages"></div>
    <div id="input-area">
      <input type="text" id="input" placeholder="Ask about the vibe..." autocomplete="off" />
      <button onclick="send()">Send</button>
    </div>
  </div>

  <script>
    const messages = document.getElementById('messages');
    const input = document.getElementById('input');

    function addMessage(text, type) {
      const div = document.createElement('div');
      div.className = `msg ${type}`;
      div.textContent = text;
      messages.appendChild(div);
      messages.scrollTop = messages.scrollHeight;
    }

    function removeTyping() {
      const typing = document.querySelector('.typing');
      if (typing) typing.remove();
    }

    // Load or create session
    let sessionId = localStorage.getItem('savrli_session') || null;

    async function send() {
      const prompt = input.value.trim();
      if (!prompt) return;
      addMessage(prompt, 'user');
      input.value = '';
      addMessage('...', 'ai typing');

      const res = await fetch('/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          prompt,
          session_id: sessionId  // Send session to backend
        })
      });
      const data = await res.json();
      sessionId = data.session_id;
      localStorage.setItem('savrli_session', sessionId);  // Save for next reload
      removeTyping();
      addMessage(data.response, 'ai');
    }

    input.addEventListener('keypress', e => {
      if (e.key === 'Enter') send();
    });
  </script>
</body>
</html>
    """


@app.get("/")
async def root():
    return {"message": "Savrli AI Chat API is running!"}


# Mock real-time restaurant data
def mock_restaurant_lookup(name: str, city: str = "Los Angeles"):
    data = {
        "The Rooftop at The Standard": {
            "vibe": "Sunset golden hour, chill house music, packed but fun",
            "crowd": "25–35, stylish, great for dates",
            "price": "$$$",
            "open_now": True,
            "live": "DJ tonight 8PM"
        },
        "Taco Truck on 6th": {
            "vibe": "Street energy, spicy al pastor, neon lights",
            "crowd": "Locals, quick bites",
            "price": "$",
            "open_now": True
        }
    }.get(name, {
        "vibe": "Cozy, warm lighting, great wine list",
        "crowd": "Mixed, intimate",
        "price": "$$",
        "open_now": True
    })
    return data
