---
# **Savrli AI Chat Endpoint**
---

A stateless FastAPI microservice that exposes an `/ai/chat` endpoint to generate conversational recommendations using OpenAI’s GPT-3.5-Turbo model.
It’s designed for use with the **Savrli app**, deployed on **Vercel** at:

> 🌐 **Base URL:** Your endpoint

---

## 📁 Project Structure

```
├── api
│   └── index.py
├── postman
│   └── Savrli-AI-Chat.postman_collection.json
├── requirements.txt
└── vercel.json
```

**Description:**

* `api/index.py` — Main FastAPI app file exposing `/ai/chat` and `/` routes.
* `postman/Savrli-AI-Chat.postman_collection.json` — Postman collection for testing.
* `requirements.txt` — Python dependencies.
* `vercel.json` — Vercel deployment configuration.

---

## ⚙️ Overview

This API takes a user’s text prompt and returns a contextual, conversational response generated via OpenAI’s GPT-3.5-Turbo.
No session or conversation memory is stored — each request is processed independently.

### **Endpoint**

`POST /ai/chat`

### **Request Body (JSON)**

```json
{
  "prompt": "User's text prompt",
  "top_p": 0.9,
  "frequency_penalty": 0.5,
  "presence_penalty": 0.5,
  "system": "Custom system instruction",
  "context_window": 10
}
```

#### Required Parameters

* **prompt** *(required)* — The text input from the user.
  * Must be non-empty (trimmed).
  * Max length: ~4000 characters (per OpenAI limit).

#### Optional Parameters

* **top_p** *(optional, float)* — Controls diversity via nucleus sampling. Range: 0.0 to 1.0.
  * Example: `0.9` means only the tokens comprising the top 90% probability mass are considered.
  * Default: Not set (OpenAI uses its default).

* **frequency_penalty** *(optional, float)* — Penalizes new tokens based on their existing frequency. Range: -2.0 to 2.0.
  * Positive values decrease repetition.
  * Default: Not set (OpenAI uses its default, typically 0).

* **presence_penalty** *(optional, float)* — Penalizes new tokens based on whether they appear in the text. Range: -2.0 to 2.0.
  * Positive values increase topic diversity.
  * Default: Not set (OpenAI uses its default, typically 0).

* **system** *(optional, string)* — Custom system instruction for the AI assistant.
  * Allows you to define the assistant's behavior and personality.
  * Example: `"You are a helpful coding assistant specializing in Python."`
  * Default: `"You are a helpful assistant providing conversational recommendations."`

* **context_window** *(optional, integer)* — Number of previous conversation turns to include in the prompt. Range: 0 to 50.
  * Only applies when using `session_id` for conversation history.
  * Example: `5` includes the last 5 user-assistant message pairs.
  * Default: `10` (configurable via `DEFAULT_CONTEXT_WINDOW` environment variable).

* **max_tokens** *(optional, integer)* — Maximum tokens in the response. Range: 1 to 2000.
  * Default: `1000` (configurable via `OPENAI_MAX_TOKENS` environment variable).

* **temperature** *(optional, float)* — Sampling temperature. Range: 0.0 to 2.0.
  * Higher values make output more random.
  * Default: `0.7` (configurable via `OPENAI_TEMPERATURE` environment variable).

* **model** *(optional, string)* — OpenAI model to use.
  * Default: `gpt-3.5-turbo` (configurable via `OPENAI_MODEL` environment variable).

* **session_id** *(optional, string)* — Session identifier for conversation history.
  * Enables multi-turn conversations with context.

* **stream** *(optional, boolean)* — Enable streaming response via Server-Sent Events.
  * Default: `false`

### **Response Body (JSON)**

```json
{
  "response": "AI's generated reply"
}
```

---

## 📡 API Details

| **Status Code** | **Meaning**             | **When It Occurs**                              |
| --------------- | ----------------------- | ----------------------------------------------- |
| 200             | ✅ Success               | Valid prompt processed; AI reply returned.      |
| 400             | ⚠️ Bad Request          | Empty or missing `prompt`.                      |
| 500             | ❌ Internal Server Error | OpenAI API failure, rate limit, or invalid key. |

---

## 🧪 Testing with cURL

### Basic Request

Use the **staging URL**:

```bash
curl -X POST https://{base-url}/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Recommend a quick breakfast recipe"}'
```

Example successful response:

```json
{
  "response": "How about scrambled eggs with avocado toast and a side of orange juice?"
}
```

### Advanced Request with Custom Parameters

```bash
curl -X POST https://{base-url}/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Python function to calculate fibonacci",
    "system": "You are an expert Python developer who writes clean, well-documented code.",
    "top_p": 0.9,
    "frequency_penalty": 0.3,
    "presence_penalty": 0.3,
    "temperature": 0.7,
    "max_tokens": 500
  }'
```

### Request with Conversation History

```bash
# First message
curl -X POST https://{base-url}/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is the capital of France?",
    "session_id": "user-123"
  }'

# Follow-up message with context
curl -X POST https://{base-url}/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is its population?",
    "session_id": "user-123",
    "context_window": 5
  }'
```

---



### 5. **Test Api**

#### Basic Test
```bash
curl -X POST BASE_URL/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Suggest a productivity hack"}'
```

#### Advanced Test with Parameters
```bash
curl -X POST BASE_URL/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain how AI works",
    "system": "You are a patient teacher explaining complex topics simply.",
    "top_p": 0.85,
    "temperature": 0.8,
    "max_tokens": 300
  }'
```

---

## 🚀 Deployment (Vercel)

### **vercel.json**

```json
{
  "builds": [
    { "src": "api/index.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "api/index.py" }
  ]
}
```

### Steps:

1. Push your project to GitHub.
2. Link your repo to Vercel.
3. Add your environment variables:

   **Required:**
   ```
   OPENAI_API_KEY = your-openai-api-key
   ```
   
   **Optional (with defaults):**
   ```
   OPENAI_MODEL = gpt-3.5-turbo
   OPENAI_MAX_TOKENS = 1000
   OPENAI_TEMPERATURE = 0.7
   DEFAULT_CONTEXT_WINDOW = 10
   MAX_HISTORY_PER_SESSION = 20
   ```

4. Deploy — it will be live 

---

