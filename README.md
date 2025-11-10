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
  
  **💡 Prefer automated setup?** Use our setup scripts:
  ```bash
  # Python script (Recommended)
  python3 setup.py
  
  # Or Bash script (Unix/Linux/macOS)
  ./setup.sh
  ```
  These scripts automate environment checks, dependency installation, and configuration!

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

## 🎓 New to Savrli AI?

### Visual Onboarding Guide

For a comprehensive visual guide with screenshots and troubleshooting, see:
- 📖 **[Detailed Onboarding Guide](docs/ONBOARDING_GUIDE.md)** - Step-by-step instructions with diagrams
- 🎬 **Visual Guides** - Screenshots and GIFs available in `docs/images/`

### Beginner Resources

- 🚀 **Quick Start**: Use automated setup scripts (`python3 setup.py` or `./setup.sh`)
- 🎮 **Interactive Testing**: Try the `/playground` endpoint first - no code needed!
- 🐛 **Common Issues**: Check the [Troubleshooting section](#-troubleshooting)
- 🤝 **First Contribution**: Look for issues labeled ["First Issue"](https://github.com/Savrli-Inc/Savrli-AI/issues?q=is%3Aissue+is%3Aopen+label%3A%22First+Issue%22)

---

## 📁 Project Structure

```
├── api
│   └── index.py                # Main FastAPI application with integrations
├── integrations
│   ├── __init__.py             # Plugin package
│   ├── plugin_base.py          # Base plugin interface and manager
│   ├── slack_plugin.py         # Slack integration
│   ├── discord_plugin.py       # Discord integration
│   ├── notion_plugin.py        # Notion integration
│   └── google_docs_plugin.py   # Google Docs integration
├── docs
│   ├── INTEGRATION_API.md      # Integration API documentation
│   └── PLUGIN_EXAMPLES.md      # Plugin usage examples
├── pages
│   └── playground.html         # Interactive demo/playground page
├── tests
│   ├── test_api.py             # Core API test suite
│   └── test_integrations.py   # Integration plugin tests
├── postman
│   └── Savrli-AI-Chat.postman_collection.json
├── requirements.txt            # Python dependencies
├── vercel.json                 # Vercel deployment configuration
└── README.md                   # This file
```

**Description:**

* `api/index.py` — Main FastAPI app with chat, history, and integration endpoints
* `integrations/` — Plugin-based integration system for productivity platforms
* `docs/` — Comprehensive documentation for integrations and extensions
* `pages/playground.html` — Interactive playground for testing AI features
* `tests/` — Test suite for core functionality and integrations
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

### 2. **Get Conversation History**

`GET /ai/history/{session_id}?limit=50`

Retrieve conversation history for a specific session.

### 3. **Clear Conversation History**

`DELETE /ai/history/{session_id}`

Clear all conversation history for a specific session.

### 4. **Interactive Playground**

`GET /playground`

Serves the interactive demo page for testing AI features in a browser.

### 5. **List Integrations**

`GET /integrations`

Lists all available integration plugins and their status.

### 6. **Send Integration Message**

`POST /integrations/send`

Send a message through a specific integration plugin (Slack, Discord, Notion, Google Docs).

### 7. **Process Integration Webhook**

`POST /integrations/webhook`

Process incoming webhooks from integration platforms.

### 8. **Get Integration Info**

`GET /integrations/{plugin_name}/info`

Get detailed information about a specific integration plugin.

### 9. **Platform-Specific Endpoints**

- `POST /integrations/slack/send` - Send message to Slack
- `POST /integrations/discord/send` - Send message to Discord
- `POST /integrations/notion/create` - Create Notion page
- `POST /integrations/google-docs/create` - Create Google Docs document
- `POST /integrations/google-docs/append` - Append to Google Docs document

### 10. **Health Check**

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

### **Core AI Variables**

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | - | Your OpenAI API key |
| `OPENAI_MODEL` | No | gpt-3.5-turbo | Default model for requests |
| `OPENAI_MAX_TOKENS` | No | 1000 | Default max tokens per response |
| `OPENAI_TEMPERATURE` | No | 0.7 | Default temperature (randomness) |
| `DEFAULT_CONTEXT_WINDOW` | No | 10 | Default conversation history size |
| `MAX_HISTORY_PER_SESSION` | No | 20 | Maximum messages stored per session |

### **Integration Variables**

#### Slack Integration
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SLACK_BOT_TOKEN` | No | - | Slack bot token (xoxb-...) |
| `SLACK_SIGNING_SECRET` | No | - | Slack signing secret for webhooks |
| `SLACK_ENABLED` | No | false | Enable Slack integration |

#### Discord Integration
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DISCORD_BOT_TOKEN` | No | - | Discord bot token |
| `DISCORD_APP_ID` | No | - | Discord application ID |
| `DISCORD_PUBLIC_KEY` | No | - | Discord public key for webhooks |
| `DISCORD_ENABLED` | No | false | Enable Discord integration |

#### Notion Integration
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NOTION_API_TOKEN` | No | - | Notion integration token |
| `NOTION_ENABLED` | No | false | Enable Notion integration |

#### Google Docs Integration
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GOOGLE_DOCS_CREDENTIALS` | No | - | Google service account credentials (JSON) |
| `GOOGLE_DOCS_ENABLED` | No | false | Enable Google Docs integration |

### **Example .env File**

```bash
# Core AI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.7

# Slack Integration
SLACK_BOT_TOKEN=xoxb-...
SLACK_SIGNING_SECRET=...
SLACK_ENABLED=true

# Discord Integration
DISCORD_BOT_TOKEN=...
DISCORD_APP_ID=...
DISCORD_PUBLIC_KEY=...
DISCORD_ENABLED=true

# Notion Integration
NOTION_API_TOKEN=secret_...
NOTION_ENABLED=true

# Google Docs Integration
GOOGLE_DOCS_CREDENTIALS=...
GOOGLE_DOCS_ENABLED=true
```

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

### Quick Setup Issues

#### **"OPENAI_API_KEY is not set"**
**Symptoms**: Server fails to start with error message about missing API key.

**Solutions**:
1. Create a `.env` file in the project root (use `setup.py` or `setup.sh`)
2. Add your API key: `OPENAI_API_KEY=sk-your-actual-key-here`
3. Get an API key from: https://platform.openai.com/api-keys
4. Ensure no extra spaces or quotes around the key
5. Restart the server after editing `.env`

**Common Mistakes**:
- ❌ `.env` file in wrong directory
- ❌ Spaces before/after the `=` sign
- ❌ Wrapping key in quotes (not needed)
- ✅ Correct format: `OPENAI_API_KEY=sk-proj-abc123...`

#### **"ModuleNotFoundError: No module named 'fastapi'"**
**Symptoms**: Import errors when starting the server.

**Solutions**:
```bash
# Run the setup script
python3 setup.py

# Or manually install dependencies
pip install -r requirements.txt

# If using virtual environment, activate it first
source venv/bin/activate  # Unix/macOS
venv\Scripts\activate     # Windows
```

#### **Port Already in Use (Address already in use)**
**Symptoms**: Server won't start, complains port 8000 is busy.

**Solutions**:
```bash
# Option 1: Use a different port
uvicorn api.index:app --reload --port 8001

# Option 2: Find and kill the process (Unix/macOS)
lsof -ti:8000 | xargs kill -9

# Option 3: Find and kill the process (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

### API Request Issues

#### **"AI temporarily unavailable" (503 error)**
**Symptoms**: Requests fail with 503 status code.

**Possible Causes & Solutions**:

1. **Invalid or Expired API Key**
   - Verify key at https://platform.openai.com/api-keys
   - Check that key is active and not revoked
   - Try regenerating the key

2. **API Quota Exceeded**
   - Log into OpenAI dashboard
   - Check usage and billing
   - Add payment method or upgrade plan

3. **Rate Limiting**
   - Wait 30-60 seconds and retry
   - Implement exponential backoff in your client
   - Consider upgrading your OpenAI tier

4. **Network Issues**
   - Test connectivity: `curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"`
   - Check firewall/proxy settings
   - Verify DNS resolution

#### **"temperature must be between 0.0 and 2.0" (400 error)**
**Symptoms**: Validation errors on request parameters.

**Solution**: Ensure all parameters are within valid ranges:

| Parameter | Valid Range | Default |
|-----------|-------------|---------|
| `temperature` | 0.0 - 2.0 | 0.7 |
| `max_tokens` | 1 - 2000 | 1000 |
| `top_p` | 0.0 - 1.0 | - |
| `frequency_penalty` | -2.0 - 2.0 | - |
| `presence_penalty` | -2.0 - 2.0 | - |
| `context_window` | 0 - 50 | 10 |

**Example valid request**:
```json
{
  "prompt": "Hello",
  "temperature": 0.7,
  "max_tokens": 1000,
  "top_p": 0.9
}
```

#### **Empty or Missing Responses**
**Symptoms**: API returns 200 but response is empty or malformed.

**Solutions**:
1. Check OpenAI API status: https://status.openai.com/
2. Verify your API quota hasn't been exhausted
3. Enable detailed logging: `logging.basicConfig(level=logging.DEBUG)`
4. Check for errors in server logs
5. Try a simpler prompt to isolate the issue

#### **Streaming Not Working**
**Symptoms**: Streaming responses timeout or don't arrive.

**Solutions**:
1. Ensure client supports Server-Sent Events (SSE)
2. Set request timeout to at least 30 seconds
3. Check network doesn't buffer SSE responses
4. Use example JavaScript client from docs:
```javascript
const eventSource = new EventSource('/ai/chat');
eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.done) eventSource.close();
  else if (data.content) console.log(data.content);
};
```

### Testing Issues

#### **Tests Failing**
**Symptoms**: `pytest` shows errors or failures.

**Solutions**:
```bash
# 1. Check Python version (need 3.8+)
python3 --version

# 2. Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# 3. Set test API key
export OPENAI_API_KEY=test-key-12345

# 4. Run tests with verbose output
pytest tests/ -v

# 5. Run specific test to debug
pytest tests/test_api.py::TestChatRequestValidation::test_basic_request -v
```

### Deployment Issues

#### **Vercel Deployment Fails**
**Symptoms**: Deployment errors on Vercel.

**Solutions**:
1. Verify `vercel.json` is properly configured
2. Check environment variables are set in Vercel dashboard
3. Review build logs for specific errors
4. Ensure Python runtime is compatible (3.9+ recommended)
5. Check function timeout settings (increase if needed)

#### **Environment Variables Not Loading on Vercel**
**Symptoms**: App works locally but not on Vercel.

**Solutions**:
1. Add environment variables in Vercel dashboard (Project Settings → Environment Variables)
2. Redeploy after adding variables
3. Check variable names match exactly (case-sensitive)
4. For production, set variables for "Production" environment

### Getting More Help

If you're still stuck:

1. **Check the detailed guide**: [docs/ONBOARDING_GUIDE.md](docs/ONBOARDING_GUIDE.md)
2. **Search existing issues**: [GitHub Issues](https://github.com/Savrli-Inc/Savrli-AI/issues)
3. **Ask the community**: [GitHub Discussions](https://github.com/Savrli-Inc/Savrli-AI/discussions)
4. **Report a bug**: [New Issue](https://github.com/Savrli-Inc/Savrli-AI/issues/new)

**Pro tip**: Include these details when asking for help:
- Python version (`python3 --version`)
- Operating system
- Error messages (full traceback)
- Steps to reproduce
- What you've already tried

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
