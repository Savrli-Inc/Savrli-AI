# api/index.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
from flasgger import Swagger

load_dotenv()

OPENAI_KEY = os.getenv("SERVER_API_KEY") or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_KEY) if OPENAI_KEY else None

app = Flask(__name__)
CORS(app)

# -----------------------
# ✅ SWAGGER CONFIG
# -----------------------
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Savrli AI API",
        "description": "API documentation for the Savrli AI backend.",
        "version": "1.0.0"
    }
}

swagger_config = {
    "headers": [],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs": [
        {
            "endpoint": "openapi_json",
            "route": "/api/openapi.json",
        }
    ],
    "specs_route": "/api/docs/"
}

Swagger(app, template=swagger_template, config=swagger_config)


# -----------------------
# ✅ HEALTH CHECK
# -----------------------
@app.route("/", methods=["GET"])
def health():
    return jsonify(ok=True, service="savrli-ai")


# -----------------------
# ✅ AI CHAT ENDPOINT
# -----------------------
@app.route("/api/chat", methods=["POST"])
def ai_chat():
    """
    Chat with Savrli AI
    ---
    tags:
      - AI
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: ChatRequest
          required:
            - message
          properties:
            message:
              type: string
              example: "Hello"
    responses:
      200:
        description: AI response
        schema:
          id: ChatResponse
          properties:
            response:
              type: string
    """
    data = request.get_json(silent=True) or {}
    msg = (data.get("message") or "").strip()

    if not msg:
        return jsonify(error="`message` is required"), 400

    if not client:
        return jsonify(error="OpenAI key missing"), 500

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": msg}]
        )

        ai_reply = resp.choices[0].message["content"]

        return jsonify(response=ai_reply)

    except Exception as e:
        return jsonify(error=str(e)), 500


# -----------------------
# ✅ NECESSARY FOR VERCEL
# -----------------------
def handler(request, *args, **kwargs):
    return app(request, *args, **kwargs)


if __name__ == "__main__":
    app.run()
