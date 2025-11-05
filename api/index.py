from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(app, config=swagger_config)

# Load OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/", methods=["GET"])
def home():
    return jsonify({"ok": True, "service": "savrli-ai"})


@swag_from({
    "tags": ["Chat"],
    "summary": "Ask Kai AI",
    "description": "Send a message to Savrli AI and get a response.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Hello Kai!"}
                },
                "required": ["message"]
            }
        }
    ],
    "responses": {
        200: {
            "description": "AI response",
            "schema": {
                "type": "object",
                "properties": {"response": {"type": "string"}}
            }
        }
    }
})
@app.route("/ai/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_message}]
        )

        ai_reply = response.choices[0].message["content"]
        return jsonify({"response": ai_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()
