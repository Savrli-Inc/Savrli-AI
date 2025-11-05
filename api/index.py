from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI(title="Savrli AI Chat Endpoint")

# CORS (Allow all for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Correct OpenAI client initialization
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    prompt: str

@app.post("/ai/chat")
async def chat_endpoint(request: ChatRequest):
    prompt = request.prompt.strip()

    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )

        ai_response = response.choices[0].message["content"].strip()
        return {"response": ai_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation error: {str(e)}")

@app.get("/")
def root():
    return {"message": "Savrli AI is running!"}
