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
  "prompt": "User's text prompt"
}
```

* **prompt** *(required)* — The text input from the user.
* Must be non-empty (trimmed).
* Max length: ~4000 characters (per OpenAI limit).

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

---



### 5. **Test Api**

```bash
curl -X POST BASE_URL/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Suggest a productivity hack"}'
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
3. Add your environment variable:

   ```
   OPENAI_API_KEY = your-openai-api-key
   ```
4. Deploy — it will be live 

---

