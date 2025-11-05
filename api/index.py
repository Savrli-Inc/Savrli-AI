import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger
from dotenv import load_dotenv

load_dotenv()

# Prefer your server key; fall back to OPENAI_API_KEY if set
OPENAI_KEY = os.getenv("SERVER_API_KEY") or os.getenv("OPENAI_API_KEY")

# Lazy import so build works even if lib version changes
try:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_KEY) if OPENAI_KEY else None
except Exception:
    client = None

app = Flask(__name__)
CORS(app)

swagger = Swagger(app, template={
    "info": {
        "title": "Savrli AI",
        "description": "Simple AI chat endpoint with Swagger docs",
        "version": "1.0.0"
    },
    "basePath": "/"
})

@app.route("/", methods=["GET"])
def health():
    """Health check endpoint
    ---
    responses:
      200:
        description: OK
    """
    return jsonify(ok=True, service="savrli-ai")

@app.route("/ai/chat", methods=["POST"])
def ai_chat():
    """Send a message to Savrli AI
    ---
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Plan me a fun dinner in Santa Monica"
    responses:
      200:
        description: AI response
        schema:
          type: object
          properties:
            reply:
              type: string
      400:
        description: Bad request
      500:
        description: Server error
    """
    data = request.get_json(silent=True) or {}
    msg = (data.get("message") or "").strip()
    if not msg:
        return jsonify(error="`message` is required"), 400
    if not client:
        return jsonify(error="OpenAI client not configured on server"), 500

    try:
        # Use a lightweight model; adjust as you like
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Kai, a friendly restaurant & travel assistant for Savrli."},
                {"role": "user", "content": msg}
            ],
            temperature=0.7,
            max_tokens=500
        )
        reply = resp.choices[0].message.content
        return jsonify(reply=reply)
    except Exception as e:
        return jsonify(error=str(e)), 500

# Vercel entrypoint
def handler(event, context):
    return app
