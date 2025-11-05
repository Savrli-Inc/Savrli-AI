import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

OPENAI_KEY = os.getenv("SERVER_API_KEY") or os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("Missing SERVER_API_KEY or OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_KEY)

@app.get("/")
def health():
    return {"ok": True, "service": "savrli-ai"}

@app.post("/ai/chat")
def ai_chat():
    try:
        data = request.get_json() or {}
        user_msg = (data.get("message") or "").strip()

        if not user_msg:
            return {"error": "message is required"}, 400

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=user_msg
        )

        return {"reply": response.output_text}

    except Exception as e:
        return {"error": str(e)}, 500
