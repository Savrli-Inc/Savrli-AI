# Savrli AI

A FastAPI microservice providing conversational AI capabilities using OpenAI's GPT models. Features stateless and stateful conversations with advanced features like streaming responses, conversation history, multimodal AI (vision, image generation), and customizable AI behavior.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-1.3+-orange.svg)](https://platform.openai.com/)

![Savrli AI Playground](https://github.com/user-attachments/assets/6ad4f14a-ed37-40d4-bddc-ddc0aceed238)

## 🚀 Quick Start

### Automated Setup (Recommended)

We provide automated setup scripts to streamline onboarding:

```bash
# Option 1: Python script (Recommended)
python3 setup.py

# Option 2: Bash script (Unix/Linux/macOS)
./setup.sh
```

These scripts will:
- ✅ Check your Python version (3.8+ required)
- ✅ Install all dependencies automatically
- ✅ Create a .env template file
- ✅ Run basic health checks
- ✅ Provide clear next steps

### Manual Setup

```bash
# 1. Clone the repository
git clone https://github.com/Savrli-Inc/Savrli-AI.git
cd Savrli-AI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file and add your OpenAI API key
echo "OPENAI_API_KEY=your-api-key-here" > .env

# 4. Start the server
uvicorn api.index:app --reload
```

Visit `http://localhost:8000/playground` to test the interactive UI!

## ✨ Features

- **💬 Conversational AI**: Chat with GPT-3.5, GPT-4, and GPT-4 Turbo models
- **🔄 Session Management**: Stateful conversations with conversation history
- **⚡ Streaming Responses**: Real-time token streaming with Server-Sent Events
- **👁️ Vision Analysis**: Analyze images with GPT-4 Vision
- **🎨 Image Generation**: Create AI art with DALL-E 3
- **🎙️ Audio Transcription**: Convert speech to text with Whisper (coming soon)
- **🔧 Advanced Tools**: Summarization, sentiment analysis, email drafting, workflow automation
- **🔌 Platform Integrations**: Slack, Discord, Notion, Google Docs plugins
- **📊 Interactive Playground**: Web-based UI for testing without code
- **📚 Comprehensive API**: RESTful endpoints with auto-generated Swagger docs

## 📸 Screenshots

### Interactive Playground
![Playground Overview](https://github.com/user-attachments/assets/6ad4f14a-ed37-40d4-bddc-ddc0aceed238)

### Image Generation
![Image Generation](https://github.com/user-attachments/assets/e01d31a0-8083-4e37-a353-240f01cd5e61)

## 📖 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Interactive Playground](#interactive-playground)
- [Usage Examples](#usage-examples)
- [Integrations](#integrations)
- [Testing](#testing)
- [Contributing](#contributing)
- [Documentation](#documentation)
- [License](#license)

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Step-by-Step Installation

See [docs/ONBOARDING_GUIDE.md](docs/ONBOARDING_GUIDE.md) for detailed installation instructions.

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# REQUIRED
OPENAI_API_KEY=sk-your-actual-api-key-here

# OPTIONAL (defaults shown)
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.7
DEFAULT_CONTEXT_WINDOW=10
MAX_HISTORY_PER_SESSION=20

# OPTIONAL: Integration Platform Tokens
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_SIGNING_SECRET=your-secret
SLACK_ENABLED=false

DISCORD_BOT_TOKEN=your-token
DISCORD_APP_ID=your-app-id
DISCORD_PUBLIC_KEY=your-public-key
DISCORD_ENABLED=false

NOTION_API_TOKEN=secret_your-token
NOTION_ENABLED=false

GOOGLE_DOCS_CREDENTIALS=your-credentials-json
GOOGLE_DOCS_ENABLED=false
```

**🔐 Security Note**: Never commit your `.env` file! It's already in `.gitignore`.

## 🔌 API Endpoints

### Core Chat API

#### POST `/ai/chat`
Send a message to the AI and get a response.

```bash
curl -X POST http://localhost:8000/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing in simple terms",
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 1000
  }'
```

**Request Parameters:**
- `prompt` (required): User's input text
- `model` (optional): AI model to use (default: gpt-3.5-turbo)
- `temperature` (optional): Sampling temperature 0.0-2.0 (default: 0.7)
- `max_tokens` (optional): Maximum response length (default: 1000)
- `session_id` (optional): Session identifier for conversation history
- `system` (optional): System instructions to customize AI behavior
- `stream` (optional): Enable streaming responses (default: false)

**Response:**
```json
{
  "response": "Quantum computing is a revolutionary computing paradigm...",
  "session_id": "user-123"
}
```

### Conversation History

#### GET `/ai/history/{session_id}`
Get conversation history for a session.

```bash
curl http://localhost:8000/ai/history/user-123
```

#### DELETE `/ai/history/{session_id}`
Clear conversation history for a session.

```bash
curl -X DELETE http://localhost:8000/ai/history/user-123
```

### Multimodal AI

#### POST `/ai/vision`
Analyze images with GPT-4 Vision.

```bash
curl -X POST http://localhost:8000/ai/vision \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What objects can you see in this image?",
    "image_url": "https://example.com/image.jpg"
  }'
```

#### POST `/ai/image/generate`
Generate images with DALL-E 3.

```bash
curl -X POST http://localhost:8000/ai/image/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A futuristic cityscape at sunset",
    "size": "1024x1024",
    "quality": "standard"
  }'
```

### Advanced AI Tools

#### POST `/ai/tools/summarize`
Summarize text.

#### POST `/ai/tools/sentiment`
Analyze sentiment of text.

#### POST `/ai/tools/email/draft`
Draft professional emails.

#### POST `/ai/tools/workflow/suggest`
Suggest automated workflows.

### Model Management

#### GET `/ai/models`
List available AI models.

#### GET `/ai/models/{model_id}`
Get details about a specific model.

### Interactive UI

#### GET `/playground`
Access the interactive playground web interface.

#### GET `/dashboard`
View analytics dashboard.

#### GET `/docs`
View auto-generated API documentation (Swagger UI).

## 🎮 Interactive Playground

Visit `http://localhost:8000/playground` after starting the server to access an interactive web interface where you can:

- **Test AI features** without writing code
- **Switch between modes**: Chat, Vision, Image Generation
- **Configure parameters**: Model, temperature, max tokens, etc.
- **View conversation history** with markdown and syntax highlighting
- **Monitor usage stats**: Message count, response times, activity charts
- **Export conversations** for reference

The playground is perfect for:
- First-time users exploring the API
- Testing different AI models and parameters
- Prototyping AI features
- Demonstrating capabilities to stakeholders

## 💻 Usage Examples

### Python

```python
import requests

# Basic chat
response = requests.post(
    "http://localhost:8000/ai/chat",
    json={"prompt": "Tell me a joke"}
)
print(response.json()["response"])

# With conversation history
response = requests.post(
    "http://localhost:8000/ai/chat",
    json={
        "prompt": "What did I just ask you?",
        "session_id": "user-123"
    }
)
print(response.json()["response"])

# Vision analysis
response = requests.post(
    "http://localhost:8000/ai/vision",
    json={
        "prompt": "Describe this image",
        "image_url": "https://example.com/photo.jpg"
    }
)
print(response.json()["response"])

# Image generation
response = requests.post(
    "http://localhost:8000/ai/image/generate",
    json={
        "prompt": "A serene mountain landscape at sunrise",
        "size": "1024x1024",
        "quality": "hd"
    }
)
print(response.json()["images"][0]["url"])
```

### JavaScript

```javascript
// Basic chat
const response = await fetch('http://localhost:8000/ai/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    prompt: 'Explain async/await in JavaScript'
  })
});
const data = await response.json();
console.log(data.response);

// Streaming response
const response = await fetch('http://localhost:8000/ai/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    prompt: 'Tell me a long story',
    stream: true
  })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const {done, value} = await reader.read();
  if (done) break;
  
  const chunk = decoder.decode(value);
  const lines = chunk.split('\n').filter(line => line.trim());
  
  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = JSON.parse(line.slice(6));
      if (data.content) {
        process.stdout.write(data.content);
      }
    }
  }
}
```

### curl

```bash
# Basic request
curl -X POST http://localhost:8000/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, how are you?"}'

# With all parameters
curl -X POST http://localhost:8000/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain machine learning",
    "model": "gpt-4",
    "temperature": 0.5,
    "max_tokens": 500,
    "session_id": "user-123",
    "system": "You are a patient teacher"
  }'

# Get conversation history
curl http://localhost:8000/ai/history/user-123

# Clear conversation history
curl -X DELETE http://localhost:8000/ai/history/user-123
```

## 🔌 Integrations

Savrli AI supports plugins for popular platforms:

- **Slack**: Send/receive messages, handle webhooks
- **Discord**: Bot integration with slash commands
- **Notion**: Create and update pages automatically
- **Google Docs**: Document generation and updates

See [docs/INTEGRATION_API.md](docs/INTEGRATION_API.md) for integration details.

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=api --cov=integrations --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run specific test
pytest tests/test_api.py::TestChatRequestValidation::test_basic_request
```

## 🤝 Contributing

We welcome contributions! Please see:

- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [docs/ONBOARDING_GUIDE.md](docs/ONBOARDING_GUIDE.md) - Detailed setup guide
- [GitHub Issues](https://github.com/Savrli-Inc/Savrli-AI/issues) - Look for "First Issue" labels

### Quick Start for Contributors

1. **Run the setup wizard**:
   ```bash
   python3 setup.py
   ```

2. **Explore the playground**:
   Visit `http://localhost:8000/playground`

3. **Find beginner-friendly issues**:
   Look for "First Issue" labels on GitHub

4. **Make changes and test**:
   ```bash
   pytest  # Run tests
   ```

5. **Submit a pull request**!

## 📚 Documentation

- **[README.md](README.md)** - This file (overview and quick start)
- **[docs/ONBOARDING_GUIDE.md](docs/ONBOARDING_GUIDE.md)** - Detailed onboarding guide for contributors
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines and workflow
- **[docs/INTEGRATION_API.md](docs/INTEGRATION_API.md)** - Integration/plugin API documentation
- **[docs/PLUGIN_EXAMPLES.md](docs/PLUGIN_EXAMPLES.md)** - Example integration implementations
- **[docs/QUICKSTART.md](docs/QUICKSTART.md)** - Quick start guide
- **[docs/images/README.md](docs/images/README.md)** - Guidelines for screenshots and visual assets

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Questions**: [GitHub Discussions](https://github.com/Savrli-Inc/Savrli-AI/discussions)
- **Bug Reports**: [GitHub Issues](https://github.com/Savrli-Inc/Savrli-AI/issues)
- **Documentation**: See [docs/](docs/) directory
- **Email**: Contact the maintainers

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [OpenAI](https://openai.com/)
- Inspired by the open-source community

---

**Made with ❤️ by the Savrli team**
