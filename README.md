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

✅ **Multi-Modal AI** - Support for text, vision/image, and audio processing  
✅ **Model Management** - 6 pre-configured models with selection and fine-tuning  
✅ **Advanced AI Tools** - Summarization, sentiment analysis, email drafting, workflow automation  
✅ **Custom AI Behavior** - Define assistant personality via system instructions  
✅ **Conversation History** - Multi-turn conversations with session management  
✅ **Streaming Responses** - Real-time token streaming for better UX  
✅ **Advanced Controls** - Fine-tune AI output with OpenAI parameters  
✅ **Input Validation** - Comprehensive error handling and validation  
✅ **History Management** - View and clear conversation history via API  
✅ **Interactive Playground** - Visual interface for testing AI features  
✅ **Enhanced Dashboard** - Real-time metrics, analytics, and theme toggle  
✅ **Platform Integrations** - Connect with Slack, Discord, Notion, and Google Docs  
✅ **Plugin Architecture** - Extensible system for third-party integrations

---

## 🤖 Multi-Modal AI Capabilities

Savrli AI supports advanced multi-modal AI processing including text, vision/image, and audio.

### **Available Models**

- **Text Models:** GPT-3.5 Turbo, GPT-4, GPT-4 Turbo
- **Vision Models:** GPT-4 Vision Preview
- **Audio Models:** Whisper-1
- **Multimodal Models:** GPT-4 Omni

### **Model Management**

```bash
# List all available models
curl https://your-api-url/ai/models

# Get specific model info
curl https://your-api-url/ai/models/gpt-4

# List fine-tunable models
curl https://your-api-url/ai/models/fine-tunable
```

### **Vision/Image Analysis**

```bash
# Analyze an image
curl -X POST https://your-api-url/ai/vision \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Describe this image in detail",
    "image_url": "https://example.com/image.jpg",
    "model": "gpt-4-vision-preview"
  }'
```

### **Audio Transcription**

```bash
# Transcribe audio
curl -X POST https://your-api-url/ai/audio/transcribe \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://example.com/audio.mp3",
    "language": "en"
  }'
```

### **Fine-Tuning Configuration**

```bash
# Configure model fine-tuning
curl -X POST https://your-api-url/ai/fine-tuning/configure \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "training_file": "file-abc123",
    "n_epochs": 3
  }'
```

---

## 🛠️ Advanced AI Tools

Savrli AI includes powerful AI-powered tools for common tasks.

### **Text Summarization**

```bash
# Summarize text
curl -X POST https://your-api-url/ai/tools/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your long text here...",
    "max_length": 128,
    "style": "concise"
  }'
```

**Styles:** `concise`, `detailed`, `bullet_points`

### **Sentiment Analysis**

```bash
# Analyze sentiment
curl -X POST https://your-api-url/ai/tools/sentiment \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I love this product!",
    "detailed": true
  }'
```

**Returns:** Sentiment (positive/negative/neutral), score (0-100), emotions, tone

### **Email Drafting**

```bash
# Generate email draft
curl -X POST https://your-api-url/ai/tools/email/draft \
  -H "Content-Type: application/json" \
  -d '{
    "purpose": "Follow up on meeting",
    "tone": "professional",
    "length": "medium",
    "key_points": ["Discuss next steps", "Schedule follow-up"]
  }'
```

**Tones:** `professional`, `casual`, `friendly`, `formal`  
**Lengths:** `short`, `medium`, `long`

### **Workflow Automation**

```bash
# Get workflow suggestions
curl -X POST https://your-api-url/ai/tools/workflow/suggest \
  -H "Content-Type: application/json" \
  -d '{
    "task_description": "Deploy application to production",
    "constraints": ["Must complete in 2 hours"],
    "tools_available": ["GitHub Actions", "Docker", "AWS"]
  }'
```

### **List All Tools**

```bash
# Get all available tools
curl https://your-api-url/ai/tools
```

---

## 📊 Enhanced Dashboard

Access the comprehensive dashboard for real-time monitoring and management.

### **Access the Dashboard**

```
http://localhost:8000/dashboard
# or
https://your-project.vercel.app/dashboard
```

### **Dashboard Features**

🎨 **Theme Toggle** - Switch between light and dark modes  
📈 **Real-Time Statistics** - Track requests, models, response times, and sessions  
🤖 **Model Overview** - View all available models with capabilities  
📊 **Usage Analytics** - Visual charts showing tool usage distribution  
⚡ **Performance Metrics** - Monitor API health and model availability  
🔌 **Integration Status** - Track status of all platform integrations  
📱 **Responsive Design** - Optimized for desktop, tablet, and mobile  
🔄 **Auto-Refresh** - Live updates every 10 seconds

### **Dashboard Sections**

1. **Statistics Cards** - Quick metrics overview
2. **Available Models** - Model registry with filtering
3. **Recent Activity** - Activity feed with timestamps
4. **Usage by Tool** - Visual progress bars
5. **AI Tools** - Tool status and descriptions
6. **Performance Metrics** - Health indicators
7. **Integration Status** - Platform connection status

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

### **Core Chat Endpoints**

### 1. **Chat Endpoint**

`POST /ai/chat`

Main endpoint for generating AI responses with full feature support.

### 2. **Get Conversation History**

`GET /ai/history/{session_id}?limit=50`

Retrieve conversation history for a specific session.

### 3. **Clear Conversation History**

`DELETE /ai/history/{session_id}`

Clear all conversation history for a specific session.

---

### **Multi-Modal AI Endpoints**

### 4. **List AI Models**

`GET /ai/models?model_type=text`

List all available AI models with optional filtering by type.

### 5. **Get Model Information**

`GET /ai/models/{model_id}`

Get detailed information about a specific model.

### 6. **Analyze Image (Vision)**

`POST /ai/vision`

Analyze images using vision-capable models.

### 7. **Transcribe Audio**

`POST /ai/audio/transcribe`

Transcribe audio files using Whisper or other audio models.

### 8. **Configure Fine-Tuning**

`POST /ai/fine-tuning/configure`

Configure fine-tuning for supported models.

### 9. **List Fine-Tunable Models**

`GET /ai/models/fine-tunable`

List all models that support fine-tuning.

---

### **Advanced AI Tools Endpoints**

### 10. **List AI Tools**

`GET /ai/tools`

List all available AI tools and their capabilities.

### 11. **Summarize Text**

`POST /ai/tools/summarize`

Summarize text with configurable length and style.

### 12. **Analyze Sentiment**

`POST /ai/tools/sentiment`

Analyze sentiment and emotions in text.

### 13. **Draft Email**

`POST /ai/tools/email/draft`

Generate professional email drafts.

### 14. **Suggest Workflow**

`POST /ai/tools/workflow/suggest`

Get AI-suggested workflows for tasks.

---

### **Dashboard & Playground**

### 15. **Interactive Playground**

`GET /playground`

Serves the interactive demo page for testing AI features in a browser.

### 16. **Enhanced Dashboard**

`GET /dashboard`

Serves the comprehensive dashboard with real-time metrics and analytics.

---

### **Integration Endpoints**

### 17. **List Integrations**

`GET /integrations`

Lists all available integration plugins and their status.

### 18. **Send Integration Message**

`POST /integrations/send`

Send a message through a specific integration plugin (Slack, Discord, Notion, Google Docs).

### 19. **Process Integration Webhook**

`POST /integrations/webhook`

Process incoming webhooks from integration platforms.

### 20. **Get Integration Info**

`GET /integrations/{plugin_name}/info`

Get detailed information about a specific integration plugin.

### 21. **Platform-Specific Endpoints**

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

For detailed guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 🗺️ Roadmap

Savrli AI is continuously evolving. Here's what we're working on:

### ✅ **Version 2.0 (Current)**
- Multi-modal AI support (text, vision, audio)
- Advanced AI tools (summarization, sentiment, email, workflow)
- Enhanced dashboard with real-time metrics
- Model management and fine-tuning
- 6 pre-configured AI models

### 🔜 **Version 2.1 (Next)**
- Complete API reference documentation
- Expanded integration examples
- Tutorial videos and guides
- Community templates

### 💡 **Version 3.0 (Future)**
- Real-time analytics and monitoring
- Workflow builder UI
- Enhanced security features
- Team collaboration
- Mobile applications

For detailed roadmap and milestones, see [ROADMAP.md](ROADMAP.md).

---

## ⭐ Key Features at a Glance

| Feature | Description | Status |
|---------|-------------|--------|
| Multi-Modal AI | Text, vision, audio processing | ✅ Available |
| Model Management | 6 models with selection & fine-tuning | ✅ Available |
| Text Summarization | 3 styles, configurable length | ✅ Available |
| Sentiment Analysis | Detailed emotion & tone analysis | ✅ Available |
| Email Drafting | Professional email generation | ✅ Available |
| Workflow Automation | AI-suggested task workflows | ✅ Available |
| Dashboard | Real-time metrics & analytics | ✅ Available |
| Slack Integration | Messages, events, commands | ✅ Available |
| Discord Integration | Messages, webhooks, interactions | ✅ Available |
| Notion Integration | Pages, databases management | ✅ Available |
| Google Docs | Document creation & editing | ✅ Available |
| Real-time Analytics | Usage tracking & monitoring | 🔜 Coming Soon |
| Mobile Apps | iOS & Android | 🔮 Planned |

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
