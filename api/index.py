# api/index.py
import os
import json
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler

from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger
from dotenv import load_dotenv

load_dotenv()

# ----------------------------------------------------------------------
# 1. Your existing Flask app (unchanged)
# ----------------------------------------------------------------------
OPENAI_KEY = os.getenv("SERVER_API_KEY") or os.getenv("OPENAI_API_KEY")

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


# ----------------------------------------------------------------------
# 2. NEW: Serve /apidocs/ (HTML) and /openapi.json (OpenAPI spec)
# ----------------------------------------------------------------------
@app.route("/apidocs", methods=["GET"])
@app.route("/apidocs/", methods=["GET"])
def apidocs():
    html = """
    <h1>Savrli AI - API Documentation</h1>
    <p>Use the interactive Swagger UI below or <a href="/swagger.json">download the OpenAPI spec</a>.</p>
    <div id="swagger"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
    <script>
      SwaggerUIBundle({ url: '/swagger.json', dom_id: '#swagger' });
    </script>
    """
    return html, 200, {'Content-Type': 'text/html'}


@app.route("/openapi.json", methods=["GET"])
@app.route("/swagger.json", methods=["GET"])
def openapi_spec():
    # Flasgger already builds the spec – just return it
    return jsonify(swagger.get_spec()), 200, {'Content-Type': 'application/json'}


# ----------------------------------------------------------------------
# 3. Vercel serverless entrypoint (unchanged)
# ----------------------------------------------------------------------
def handler(event, context):
    # Vercel expects a WSGI-compatible callable – Flask provides one via `app`
    return app
