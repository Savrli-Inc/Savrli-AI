import os
from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from

# Optional: OpenAI (will only be used if SERVER_API_KEY is present)
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

app = Flask(__name__)

# ---- Swagger UI config ----
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "Savrli AI API",
        "description": "Endpoints for Savrli AI. Use **/apidocs** to test.",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": ["https", "http"]
})

@app.route("/", methods=["GET"])
def health():
    """Health check
    ---
    tags:
      - System
    responses:
      200:
        description: OK
        schema:
          type: object
          properties:
            ok:
              type: boolean
            service:
              type: string
    """
    return jsonify({"ok": True, "service": "savrli-ai"})

@app.route("/ai/chat", methods=["POST"])
@swag_from({
    "tags": ["AI"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "parameters": [
        {
            "in": "body",
            "name": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Hello, can you help me plan a date in Santa Monica?"},
                    "system": {"type": "string", "example": "You are Kai, Savrli's helpful dining assistant."}
                },
                "required": ["message"]
            }
        }
    ],
    "responses": {
        "200": {
            "description": "AI response",
            "schema": {
                "type": "object",
                "properties": {
                    "reply": {"type": "string"}
                }
            }
        },
        "400": {"description": "Bad request / missing key"},
        "500": {"description": "Server error"}
    }
})
def ai_chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    system = data.get("system") or "You are a concise, helpful assistant."

    if not message:
        return jsonify({"error": "message is required"}), 400

    api_key = os.getenv("SERVER_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        # Still return something helpful if key isn't set yet
        return jsonify({"reply": f"(mock) You said: {message}"}), 200

    if OpenAI is None:
        return jsonify({"error": "OpenAI SDK not installed"}), 500

    try:
        client = OpenAI(api_key=api_key)

        # Using the Responses API (OpenAI Python SDK v1+)
        resp = client.responses.create(
            model="gpt-4o-mini",
            input=f"{system}\n\nUser: {message}"
        )
        reply = resp.output_text or ""

        return jsonify({"reply": reply}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Vercel entrypoint
def handler(request, *args, **kwargs):
    return app.wsgi_app(request.environ, start_response=None)

if __name__ == "__main__":
    # Local dev (Vercel won’t use this block)
    app.run(host="0.0.0.0", port=3000)
