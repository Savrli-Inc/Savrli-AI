---
# **Savrli AI Chat Endpoint**
---

A powerful FastAPI microservice that provides conversational AI capabilities using OpenAI's GPT models.
It supports both stateless and stateful conversations with advanced features like streaming responses, conversation history, and customizable AI behavior.
Designed for use with the **Savrli app**, deployed on **Vercel**.

> 🌐 **Base URL:** Your endpoint

---

## 🚀 Quick Start Onboarding Checklist

New to Savrli AI? Follow this checklist to get up and running:

- [ ] **Step 1:** Clone the repository
  ```bash
  git clone https://github.com/Savrli-Inc/Savrli-AI.git
  cd Savrli-AI
  ```

- [ ] **Step 2:** Install dependencies
  ```bash
  pip install -r requirements.txt
  ```

- [ ] **Step 3:** Set up environment variables
  - Create a `.env` file in the project root
  - Add your OpenAI API key:
    ```
    OPENAI_API_KEY=your-api-key-here
    ```
  - Optional environment variables:
    ```
    OPENAI_MODEL=gpt-3.5-turbo
    OPENAI_MAX_TOKENS=1000
    OPENAI_TEMPERATURE=0.7
    DEFAULT_CONTEXT_WINDOW=10
    MAX_HISTORY_PER_SESSION=20
    ```

- [ ] **Step 4:** Run the API locally
  ```bash
  uvicorn api.index:app --reload
  ```
  The API will be available at `http://localhost:8000`

- [ ] **Step 5:** Try the interactive playground (recommended for new users)
  - Open `http://localhost:8000/playground` in your browser
  - Use the visual interface to test AI features without writing code

- [ ] **Step 6:** Test with a basic request
  ```bash
  curl -X POST http://localhost:8000/ai/chat \
    -H "Content-Type: application/json" \
    -d '{"prompt": "Hello, how are you?"}'
  ```

- [ ] **Step 7:** Deploy to Vercel (see [Deployment section](#-deployment-vercel))

- [ ] **Step 8:** Test your deployed endpoint with the sample requests below

---

## 📁 Project Structure

```
├── api
│   └── index.py           # Main FastAPI application
├── pages
│   └── playground.html    # Interactive demo/playground page
├── tests
│   └── test_api.py        # Comprehensive test suite
├── postman
│   └── Savrli-AI-Chat.postman_collection.json
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel deployment configuration
└── README.md             # This file
```

**Description:**

* `api/index.py` — Main FastAPI app exposing chat and history management endpoints
* `pages/playground.html` — Interactive playground for testing AI features in a browser
* `tests/test_api.py` — Test suite for validation and functionality
* `postman/Savrli-AI-Chat.postman_collection.json` — Postman collection for testing
* `requirements.txt` — Python dependencies
* `vercel.json` — Vercel deployment configuration

---

## ⚙️ Overview

This API takes a user's text prompt and returns a contextual, conversational response generated via OpenAI's GPT models.
The API supports both stateless (one-off) and stateful (session-based) conversations with conversation history tracking.

### **Core Features**

✅ **Custom AI Behavior** - Define assistant personality via system instructions  
✅ **Conversation History** - Multi-turn conversations with session management  
✅ **Streaming Responses** - Real-time token streaming for better UX  
✅ **Advanced Controls** - Fine-tune AI output with OpenAI parameters  
✅ **Input Validation** - Comprehensive error handling and validation  
✅ **History Management** - View and clear conversation history via API  
✅ **Interactive Playground** - Visual interface for testing AI features  
✅ **Text Summarization** - AI-powered text summarization with customizable length  
✅ **Sentiment Analysis** - Analyze emotional tone and sentiment of text  
✅ **Email Drafting** - Generate professional emails with customizable tone and purpose  
✅ **Platform Integrations** - Connect with Slack, Discord, Notion, and Google Docs  
✅ **Plugin Architecture** - Extensible system for third-party integrations  

---

## 🔌 Platform Integrations

Savrli AI now supports integration with popular productivity platforms through a flexible plugin architecture.

### **Supported Platforms**

- **Slack** - Send messages, process events, handle slash commands
- **Discord** - Send messages, process interactions, manage webhooks
- **Notion** - Create/update pages, manage databases
- **Google Docs** - Create/update documents, format text

### **Quick Integration Example**

```bash
# Send AI-generated message to Slack
curl -X POST https://your-api-url/integrations/slack/send \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "#general",
    "message": "Hello from Savrli AI!"
  }'
```

### **Integration Documentation**

- 📚 [Integration API Documentation](docs/INTEGRATION_API.md)
- 💡 [Plugin Examples](docs/PLUGIN_EXAMPLES.md)
- 🛠️ [Third-Party Extension Guide](docs/INTEGRATION_API.md#third-party-extension-guide)

---

## 🎮 Interactive Playground

The Savrli AI Playground provides a user-friendly web interface for testing and experimenting with AI capabilities without writing code.

### **Access the Playground**

Once your server is running, visit:
```
http://localhost:8000/playground
```

Or on your deployed Vercel instance:
```
https://your-project.vercel.app/playground
```

### **Playground Features**

🎯 **Model Selection** - Choose between GPT-3.5 Turbo, GPT-4, and GPT-4 Turbo  
⚙️ **Parameter Controls** - Adjust temperature, max tokens, and other OpenAI parameters  
💬 **Conversation History** - Maintain context across multiple messages  
🎨 **System Instructions** - Customize AI personality and behavior  
📊 **Real-time Feedback** - See loading states and error messages  
📱 **Responsive Design** - Works on desktop, tablet, and mobile devices  

### **Perfect For**

- **Onboarding**: New users can understand AI capabilities through hands-on interaction
- **Testing**: Quickly validate API functionality and response quality
- **Demos**: Showcase AI features to stakeholders without technical setup
- **Experimentation**: Try different parameters and prompts to optimize results

### **Contributing to the Playground**

The playground is built with vanilla HTML/CSS/JavaScript for easy customization:

- **Styling**: Update CSS variables in `pages/playground.html` to match your brand
- **API Endpoint**: Modify `API_ENDPOINT` constant for different backends
- **New Parameters**: Add inputs in HTML and capture in `buildRequestBody()` function
- **UI Enhancements**: The code includes inline comments to guide modifications

---

## 🔌 API Endpoints

### 1. **Chat Endpoint**

`POST /ai/chat`

Main endpoint for generating AI responses with full feature support.

### 2. **Text Summarization**

`POST /ai/summarize`

Summarize long texts into concise summaries using AI.

### 3. **Sentiment Analysis**

`POST /ai/sentiment`

Analyze the emotional tone and sentiment of text.

### 4. **Email Drafting**

`POST /ai/draft-email`

Generate professional email drafts based on context and requirements.

### 5. **Get Conversation History**

`GET /ai/history/{session_id}?limit=50`

Retrieve conversation history for a specific session.

### 6. **Clear Conversation History**

`DELETE /ai/history/{session_id}`

Clear all conversation history for a specific session.

### 7. **Interactive Playground**

`GET /playground`

Serves the interactive demo page for testing AI features in a browser.

### 8. **Health Check**

`GET /`

Returns API status confirmation.

---

## 📝 Request Parameters

### **Required Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | string | User's text input (required, non-empty) |

### **Optional Parameters**

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `session_id` | string | - | None | Session identifier for conversation history |
| `system` | string | - | Default assistant | Custom system instruction defining AI behavior |
| `stream` | boolean | - | false | Enable Server-Sent Events streaming |
| `model` | string | - | gpt-3.5-turbo | OpenAI model to use |
| `max_tokens` | integer | 1-2000 | 1000 | Maximum tokens in response |
| `temperature` | float | 0.0-2.0 | 0.7 | Sampling temperature (higher = more random) |
| `top_p` | float | 0.0-1.0 | - | Nucleus sampling parameter |
| `frequency_penalty` | float | -2.0 to 2.0 | - | Penalize token frequency (reduce repetition) |
| `presence_penalty` | float | -2.0 to 2.0 | - | Penalize token presence (increase diversity) |
| `context_window` | integer | 0-50 | 10 | Number of previous conversation turns to include |

---

## 📡 Response Codes & Error Handling

| Status Code | Meaning | When It Occurs | Example Response |
|-------------|---------|----------------|------------------|
| **200** | ✅ Success | Valid request processed successfully | `{"response": "AI reply", "session_id": "user-123"}` |
| **400** | ⚠️ Bad Request | Invalid input parameters | `{"detail": "Prompt cannot be empty"}` |
| **400** | ⚠️ Bad Request | Parameter out of range | `{"detail": "temperature must be between 0.0 and 2.0"}` |
| **400** | ⚠️ Bad Request | Invalid max_tokens | `{"detail": "max_tokens must be between 1 and 2000"}` |
| **400** | ⚠️ Bad Request | Invalid top_p | `{"detail": "top_p must be between 0.0 and 1.0"}` |
| **400** | ⚠️ Bad Request | Invalid frequency_penalty | `{"detail": "frequency_penalty must be between -2.0 and 2.0"}` |
| **400** | ⚠️ Bad Request | Invalid presence_penalty | `{"detail": "presence_penalty must be between -2.0 and 2.0"}` |
| **400** | ⚠️ Bad Request | Invalid context_window | `{"detail": "context_window must be between 0 and 50"}` |
| **502** | ❌ Bad Gateway | OpenAI returned unexpected response format | `{"detail": "AI returned an empty response"}` |
| **503** | ❌ Service Unavailable | OpenAI API failure, rate limit, or network issue | `{"detail": "AI temporarily unavailable"}` |

### **Common Error Scenarios**

1. **Empty Prompt**: Submit a non-empty prompt string
2. **Invalid Temperature**: Use a value between 0.0 and 2.0
3. **OpenAI API Issues**: Check your API key and quota
4. **Rate Limiting**: Implement retry logic with exponential backoff

---

## 🧪 Example Requests

### **1. Basic Chat Request**

Simple one-off conversation without history.

```bash
curl -X POST https://your-api-url/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Recommend a quick breakfast recipe"
  }'
```

**Response:**
```json
{
  "response": "How about scrambled eggs with avocado toast and a side of orange juice?",
  "session_id": null
}
```

---

### **2. Chat with Custom System Instructions**

Define the AI's personality and expertise.

```bash
curl -X POST https://your-api-url/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Python function to calculate fibonacci",
    "system": "You are an expert Python developer who writes clean, well-documented code."
  }'
```

---

### **3. Conversational Chat with History**

Multi-turn conversation with context awareness.

```bash
# First message
curl -X POST https://your-api-url/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is the capital of France?",
    "session_id": "user-123"
  }'

# Follow-up message (AI remembers previous context)
curl -X POST https://your-api-url/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is its population?",
    "session_id": "user-123"
  }'
```

---

### **4. Advanced Request with All Parameters**

Fine-tuned AI behavior with custom parameters.

```bash
curl -X POST https://your-api-url/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing simply",
    "system": "You are a patient teacher explaining complex topics to beginners.",
    "session_id": "user-456",
    "model": "gpt-3.5-turbo",
    "temperature": 0.8,
    "top_p": 0.9,
    "frequency_penalty": 0.3,
    "presence_penalty": 0.3,
    "max_tokens": 500,
    "context_window": 5
  }'
```

---

### **5. Streaming Response**

Get real-time streaming responses using Server-Sent Events.

```bash
curl -X POST https://your-api-url/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Tell me a short story",
    "stream": true
  }'
```

**Response (SSE format):**
```
data: {"content": "Once"}

data: {"content": " upon"}

data: {"content": " a"}

data: {"content": " time"}

data: {"done": true}
```

**JavaScript Example for Streaming:**
```javascript
const eventSource = new EventSource('/ai/chat');
eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.done) {
    eventSource.close();
  } else if (data.content) {
    console.log(data.content); // Append to UI
  } else if (data.error) {
    console.error(data.error);
    eventSource.close();
  }
};
```

---

### **6. Get Conversation History**

Retrieve conversation history for a session.

```bash
curl -X GET https://your-api-url/ai/history/user-123?limit=10
```

**Response:**
```json
{
  "session_id": "user-123",
  "messages": [
    {
      "role": "user",
      "content": "What is the capital of France?",
      "timestamp": "2025-11-08T12:00:00.000Z"
    },
    {
      "role": "assistant",
      "content": "The capital of France is Paris.",
      "timestamp": "2025-11-08T12:00:01.000Z"
    }
  ],
  "total_messages": 2
}
```

---

### **7. Clear Conversation History**

Delete all conversation history for a session.

```bash
curl -X DELETE https://your-api-url/ai/history/user-123
```

**Response:**
```json
{
  "message": "History cleared for session user-123"
}
```

---

### **8. Text Summarization**

Summarize long texts into concise summaries.

```bash
curl -X POST https://your-api-url/ai/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of intelligent agents: any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. Colloquially, the term artificial intelligence is often used to describe machines (or computers) that mimic cognitive functions that humans associate with the human mind, such as learning and problem solving."
  }'
```

**Response:**
```json
{
  "summary": "Artificial intelligence (AI) refers to machine-demonstrated intelligence that allows devices to perceive their environment and take goal-oriented actions, mimicking human cognitive functions like learning and problem solving.",
  "original_length": 73,
  "summary_length": 28
}
```

**With custom summary length:**
```bash
curl -X POST https://your-api-url/ai/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your long text here...",
    "max_length": 50
  }'
```

**Parameters:**
- `text` (required): The text to summarize
- `max_length` (optional): Target length in words for the summary
- `model` (optional): OpenAI model to use (default: gpt-3.5-turbo)

---

### **9. Sentiment Analysis**

Analyze the emotional tone and sentiment of text.

```bash
curl -X POST https://your-api-url/ai/sentiment \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I absolutely love this product! It exceeded all my expectations and the customer service was outstanding."
  }'
```

**Response:**
```json
{
  "sentiment": "positive",
  "confidence": 0.95,
  "reasoning": "The text expresses strong positive emotions with words like 'love', 'exceeded expectations', and 'outstanding'."
}
```

**Negative sentiment example:**
```bash
curl -X POST https://your-api-url/ai/sentiment \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I am very disappointed with this purchase. It did not work as advertised."
  }'
```

**Response:**
```json
{
  "sentiment": "negative",
  "confidence": 0.88,
  "reasoning": "The text conveys disappointment and dissatisfaction with the product."
}
```

**Parameters:**
- `text` (required): The text to analyze
- `model` (optional): OpenAI model to use (default: gpt-3.5-turbo)

**Response Fields:**
- `sentiment`: One of "positive", "negative", or "neutral"
- `confidence`: Float between 0.0 and 1.0 indicating confidence level
- `reasoning`: Brief explanation of the sentiment analysis

---

### **10. Email Drafting**

Generate professional email drafts based on context.

```bash
curl -X POST https://your-api-url/ai/draft-email \
  -H "Content-Type: application/json" \
  -d '{
    "context": "Need to schedule a project kickoff meeting with the development team for next week",
    "recipient": "Development Team",
    "tone": "professional"
  }'
```

**Response:**
```json
{
  "email_draft": "Subject: Project Kickoff Meeting - Next Week\n\nDear Development Team,\n\nI hope this email finds you well.\n\nI would like to schedule our project kickoff meeting for next week. This meeting will be an opportunity to discuss project objectives, timelines, and responsibilities.\n\nPlease let me know your availability for next week, and I will send out a calendar invitation accordingly.\n\nLooking forward to working with you all.\n\nBest regards",
  "tone": "professional",
  "recipient": "Development Team"
}
```

**Casual tone example:**
```bash
curl -X POST https://your-api-url/ai/draft-email \
  -H "Content-Type: application/json" \
  -d '{
    "context": "Thank a colleague for helping with a bug fix",
    "recipient": "Sarah",
    "tone": "casual"
  }'
```

**Formal tone with purpose:**
```bash
curl -X POST https://your-api-url/ai/draft-email \
  -H "Content-Type: application/json" \
  -d '{
    "context": "Request approval for budget increase",
    "recipient": "Finance Director",
    "tone": "formal",
    "purpose": "request"
  }'
```

**Parameters:**
- `context` (required): Description of what the email is about
- `recipient` (optional): Who the email is addressed to
- `tone` (optional): One of "professional", "casual", "formal", or "friendly" (default: "professional")
- `purpose` (optional): Type of email such as "request", "response", "update", etc.
- `model` (optional): OpenAI model to use (default: gpt-3.5-turbo)

**Response Fields:**
- `email_draft`: The complete email including subject line, greeting, body, and closing
- `tone`: The tone used for the email
- `recipient`: The recipient specified (if provided)

---

## 🚀 Deployment (Vercel)

### **Prerequisites**

1. GitHub account with your repository
2. Vercel account (free tier works)
3. OpenAI API key

### **Deployment Steps**

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Link to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import your GitHub repository

3. **Configure Environment Variables**
   
   In Vercel dashboard, add these environment variables:
   
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

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Your API will be live at `https://your-project.vercel.app`

5. **Test Deployment**
   ```bash
   curl -X POST https://your-project.vercel.app/ai/chat \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello!"}'
   ```

### **vercel.json Configuration**

The project includes a `vercel.json` file that configures the deployment:

```json
{
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

---

## 🧰 Environment Variables

Configure these in your `.env` file for local development or in Vercel dashboard for production:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | - | Your OpenAI API key |
| `OPENAI_MODEL` | No | gpt-3.5-turbo | Default model for requests |
| `OPENAI_MAX_TOKENS` | No | 1000 | Default max tokens per response |
| `OPENAI_TEMPERATURE` | No | 0.7 | Default temperature (randomness) |
| `DEFAULT_CONTEXT_WINDOW` | No | 10 | Default conversation history size |
| `MAX_HISTORY_PER_SESSION` | No | 20 | Maximum messages stored per session |

---

## 🧪 Testing

### **Run Tests Locally**

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
python -m pytest tests/ -v

# Run specific test class
python -m pytest tests/test_api.py::TestChatRequestValidation -v

# Run with coverage
python -m pytest tests/ --cov=api --cov-report=html
```

### **Test Coverage**

The test suite covers:
- ✅ Input validation for all parameters
- ✅ Error handling and edge cases
- ✅ Custom system instructions
- ✅ Conversation history management
- ✅ Advanced OpenAI parameters
- ✅ Backwards compatibility

---

## 🔧 Troubleshooting

### **Issue: "OPENAI_API_KEY is not set"**
**Solution:** Set the environment variable in `.env` file or Vercel dashboard.

### **Issue: "AI temporarily unavailable" (503 error)**
**Solution:** Check your OpenAI API key, quota, and network connectivity.

### **Issue: "temperature must be between 0.0 and 2.0" (400 error)**
**Solution:** Ensure all parameters are within valid ranges (see [Request Parameters](#-request-parameters)).

### **Issue: Empty or missing responses**
**Solution:** Check OpenAI API status and your API quota. Enable logging to see detailed errors.

### **Issue: Streaming not working**
**Solution:** Ensure your client supports Server-Sent Events (SSE). Check the streaming example above.

---

## 📚 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vercel Python Deployment](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Server-Sent Events (SSE)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes and add tests
4. Run tests to ensure everything passes
5. Commit your changes (`git commit -m 'Add new feature'`)
6. Push to your branch (`git push origin feature/your-feature`)
7. Open a Pull Request

---

## 📄 License

This project is part of the Savrli platform. All rights reserved.

---

## 🔗 Links

- **Repository:** [Savrli-Inc/Savrli-AI](https://github.com/Savrli-Inc/Savrli-AI)
- **Issues:** [Report an issue](https://github.com/Savrli-Inc/Savrli-AI/issues)
- **Discussions:** [Join the discussion](https://github.com/Savrli-Inc/Savrli-AI/discussions)

---

**Made with ❤️ by the Savrli Team**
