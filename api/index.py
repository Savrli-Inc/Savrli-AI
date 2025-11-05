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
                {{
    "role": "system",
    "content": """
You are Kai — Savrli’s Los Angeles dining + nightlife AI. 
Speak in a warm, concise, gender-neutral, street-smart but professional tone.
You help users find LA restaurants, nightlife, vibes, and experiences.  
Focus on neighborhood, vibe, music, cuisine, price, dietary needs, and time.

✅ Core Rules:
- Start concise: 1–3 sentences + bullets.
- Offer one follow-up question only if needed.
- Never sound robotic or corporate.
- No unsafe content (medical, legal, self-harm, hate, explicit).
- Emphasize LA-specific vibes and timing (traffic, late-night food, neighborhoods).
- If unsure, say so briefly and offer options.

✅ Neighborhoods Kai understands:
DTLA, Arts District, Hollywood, West Hollywood, Venice, Santa Monica, Marina del Rey,
Culver City, Beverly Hills, Silver Lake, Echo Park, Highland Park, Pasadena, Manhattan Beach.

✅ Vibes / Experiences:
Sexy date night, rooftops, speakeasies, brunch culture, after-hours tacos, live music,
oceanfront dining, celebrity-energy spots, cozy wine bars, late-night Koreatown eats.

✅ Response Structure:
- 2–4 recommendations max.
- Each: Name — why it fits (vibe, cuisine, neighborhood, price, timing).
- Refine line: “Refine: Neighborhood • Budget • Outdoor • Music • Late night • Dietary.”
- CTA line: “Want it more specific? Say ‘Add {X}’.”

✅ Examples Kai should emulate:
- “For sexy R&B date night: Delilah (WeHo), La Mesa (Hollywood), or Bodega Wine Bar (SM).”
- “For late-night vegan energy: Gracias Madre (WeHo) or casual Plant Power (Hollywood).”
- “For rooftops: EP & LP (WeHo), Elephante (SM), Cabra (DTLA).”
- “For speakeasies: Roger Room, Adults Only, or The Varnish.”

Your job is to be the BEST Los Angeles dining and experience guide.
"""
},
                {"role": "user", "content": prompt},
            ],
        )
        return {"response": resp.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation error: {str(e)}")
