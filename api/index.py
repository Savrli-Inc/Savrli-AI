import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Health check so visiting the root never crashes ---
@app.get("/")
def health():
    return jsonify({"ok": True, "service": "savrli-ai"}), 200

# --- Chat endpoint (POST) ---
@app.post("/ai/chat")
def chat():
    # Require server key header so random traffic can't hit OpenAI
    server_key = os.getenv("SERVER_API_KEY")
    if not server_key:
        return jsonify({"error": "SERVER_API_KEY not configured"}), 500

    header_key = request.headers.get("x-api-key")
    if header_key != server_key:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    user_msg = (data.get("message") or "").strip()
    if not user_msg:
        return jsonify({"error": "message is required"}), 400

    try:
        # OpenAI SDK v1 style
        from openai import OpenAI
        client = OpenAI()  # uses OPENAI_API_KEY from env
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Kai, a concise and friendly dining assistant."},
                {"role": "user", "content": user_msg}
            ]
        )
        answer = resp.choices[0].message.content
        return jsonify({"reply": answer}), 200
    except Exception as e:
        # Never crash the process — return the error instead
        return jsonify({"error": str(e)}), 500
