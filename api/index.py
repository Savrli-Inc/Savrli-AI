# api/index.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_KEY = os.getenv("SERVER_API_KEY") or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_KEY) if OPENAI_KEY else None

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def health():
    return jsonify(ok=True, service="savrli-ai")

@app.route("/ai/chat", methods=["POST"])
def ai_chat():
    data = request.get_json(silent=True) or {}
    msg = (data.get("message") or "").strip()
    if not msg:
        return jsonify(error="`message` is required"), 400
    if not client:
        return jsonify(error="OpenAI key missing"), 500
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
        return jsonify(reply=resp.choices[0].message.content)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route("/apidocs", methods=["GET"])
@app.route("/apidocs/", methods=["GET"])
def apidocs():
    return """
    <h1>Savrli AI - API Docs</h1>
    <p><strong>POST /ai/chat</strong></p>
    <pre>
{
  "message": "Your question here"
}
    </pre>
    <p><strong>Returns:</strong></p>
    <pre>
{
  "reply": "AI response"
}
    </pre>
    <hr>
    <small>Health: <a href="/">/</a> → {"ok": true}</small>
    """, 200, {'Content-Type': 'text/html'}

def handler(event, context):
    from flask_awscgi import FlaskAWS
    return FlaskAWS(app)(event, context)
