# Savrli AI Onboarding Guide

Welcome to Savrli AI! 🚀 This guide will help you get started quickly and efficiently.

## Table of Contents

- [Quick Start](#quick-start)
- [Visual Guides](#visual-guides)
- [Detailed Setup](#detailed-setup)
- [Common Issues & Troubleshooting](#common-issues--troubleshooting)
- [First-Time Contributors](#first-time-contributors)
- [Learning Resources](#learning-resources)

---

## Quick Start

### Automated Setup (Recommended for Beginners)

We provide automated setup scripts to streamline your onboarding:

**Option 1: Python Script** (Recommended)
```bash
python3 setup.py
```

**Option 2: Bash Script** (For Unix/Linux/macOS users)
```bash
./setup.sh
```

These scripts will:
- ✅ Check your Python version (3.8+ required)
- ✅ Install all dependencies automatically
- ✅ Create a .env template file
- ✅ Run basic health checks
- ✅ Provide clear next steps

### Manual Setup

If you prefer to set up manually:

```bash
# 1. Clone the repository
git clone https://github.com/Savrli-Inc/Savrli-AI.git
cd Savrli-AI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
cp .env.example .env  # If example exists, otherwise create manually

# 4. Add your OpenAI API key to .env
# Edit .env and add: OPENAI_API_KEY=your-api-key-here

# 5. Run the server
uvicorn api.index:app --reload
```

---

## Visual Guides

### Setup Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Savrli AI Setup Flow                      │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │  Run setup script    │
                  │  python3 setup.py    │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │  Environment Check   │
                  │  • Python 3.8+       │
                  │  • pip installed     │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │  Install Dependencies│
                  │  pip install -r ...  │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │  Configure .env      │
                  │  Add OPENAI_API_KEY  │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │  Start Server        │
                  │  uvicorn api ...     │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │  Test in Playground  │
                  │  localhost:8000/...  │
                  └──────────────────────┘
```

### Playground Interface Preview

The interactive playground is your easiest way to test AI features without writing code:

![Playground Interface](https://github.com/user-attachments/assets/6ad4f14a-ed37-40d4-bddc-ddc0aceed238)

*Figure 1: The Savrli AI Playground interface showing chat configuration and response panels*

When you visit `http://localhost:8000/playground`, you'll see:

- **Configuration Panel** (Left): Model selection, temperature, tokens, system instructions
- **Response Panel** (Right): AI responses with markdown rendering and syntax highlighting
- **Mode Tabs**: Switch between Chat, Vision, and Image Generation
- **Stats Dashboard**: Real-time metrics showing message count, session time, and response times
- **Quick Actions**: Pre-built prompts to get started quickly

**Multimodal Features:**

![Image Generation Tab](https://github.com/user-attachments/assets/e01d31a0-8083-4e37-a353-240f01cd5e61)

*Figure 2: Image Generation tab for creating AI art with DALL-E*

The playground supports:
- 💬 **Chat Mode**: Conversational AI with GPT models
- 👁️ **Vision Mode**: Analyze images and extract information
- 🎨 **Image Generation**: Create AI art with DALL-E

> **Note**: Screenshots are available in the `docs/images/` directory. Contributors can add more screenshots and GIFs following the guidelines in `docs/images/README.md`.

---

## Detailed Setup

### Prerequisites

- **Python 3.8 or higher** - Check with `python3 --version`
- **pip** - Python package installer
- **OpenAI API Key** - Get one at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Git** - For cloning the repository

### Step-by-Step Installation

#### 1. Clone and Navigate

```bash
git clone https://github.com/Savrli-Inc/Savrli-AI.git
cd Savrli-AI
```

#### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Unix/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected packages:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `openai>=1.3.0` - OpenAI API client
- `pydantic` - Data validation
- `python-dotenv` - Environment variables
- `pytest` - Testing framework
- `httpx` - HTTP client for tests

#### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Create from template (if available)
cp .env.example .env

# Or create manually
touch .env
```

Add your configuration:

```bash
# REQUIRED
OPENAI_API_KEY=sk-your-actual-api-key-here

# OPTIONAL (defaults shown)
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.7
DEFAULT_CONTEXT_WINDOW=10
MAX_HISTORY_PER_SESSION=20
```

**🔐 Security Note**: Never commit your `.env` file! It's already in `.gitignore`.

#### 5. Verify Installation

Run the test suite:

```bash
python -m pytest tests/ -v
```

All tests should pass ✅

#### 6. Start the Server

```bash
uvicorn api.index:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

#### 7. Test Your Setup

**Option A: Use the Playground** (Easiest for beginners)
1. Open `http://localhost:8000/playground` in your browser
2. Type a message and click "Send"
3. See the AI response in real-time

**Option B: Use curl**
```bash
curl -X POST http://localhost:8000/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, how are you?"}'
```

**Option C: Use Python**
```python
import requests

response = requests.post(
    "http://localhost:8000/ai/chat",
    json={"prompt": "Hello, how are you?"}
)
print(response.json())
```

---

## Common Issues & Troubleshooting

### 🔴 "OPENAI_API_KEY is not set"

**Problem**: The server won't start because the API key is missing.

**Solution**:
1. Make sure `.env` file exists in the project root
2. Open `.env` and verify the API key is set:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```
3. Make sure there are no extra spaces or quotes
4. Restart the server after editing `.env`

**Common Mistakes**:
- ❌ `OPENAI_API_KEY = sk-...` (space before =)
- ❌ `OPENAI_API_KEY="sk-..."` (unnecessary quotes)
- ✅ `OPENAI_API_KEY=sk-...` (correct)

---

### 🔴 "ModuleNotFoundError: No module named 'fastapi'"

**Problem**: Dependencies are not installed.

**Solution**:
```bash
# Make sure you're in the project directory
cd Savrli-AI

# Install dependencies
pip install -r requirements.txt

# If using virtual environment, make sure it's activated
source venv/bin/activate  # Unix/macOS
# or
venv\Scripts\activate  # Windows
```

---

### 🔴 "AI temporarily unavailable" (503 error)

**Problem**: The server can't reach OpenAI's API.

**Possible Causes & Solutions**:

1. **Invalid API Key**
   - Check your API key at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Make sure it's active and has quota remaining
   
2. **Network Issues**
   - Check your internet connection
   - Try accessing [platform.openai.com](https://platform.openai.com) in browser
   - Check if you need proxy settings

3. **Rate Limiting**
   - Wait a few moments and try again
   - Check your OpenAI usage limits

4. **API Quota Exceeded**
   - Log into OpenAI dashboard and check your usage
   - Add payment method or upgrade plan if needed

---

### 🔴 "temperature must be between 0.0 and 2.0" (400 error)

**Problem**: Invalid parameter values in your request.

**Solution**: Check parameter ranges:
- `temperature`: 0.0 to 2.0
- `max_tokens`: 1 to 2000
- `top_p`: 0.0 to 1.0
- `frequency_penalty`: -2.0 to 2.0
- `presence_penalty`: -2.0 to 2.0
- `context_window`: 0 to 50

**Example valid request**:
```json
{
  "prompt": "Hello",
  "temperature": 0.7,
  "max_tokens": 1000
}
```

---

### 🔴 Tests Failing

**Problem**: `pytest` shows failing tests.

**Solution**:

1. **Check Python version**
   ```bash
   python3 --version  # Should be 3.8+
   ```

2. **Reinstall dependencies**
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

3. **Set test API key**
   ```bash
   export OPENAI_API_KEY=test-key-for-testing
   pytest tests/ -v
   ```

4. **Run specific test to debug**
   ```bash
   pytest tests/test_api.py::TestChatRequestValidation::test_basic_request -v
   ```

---

### 🔴 Port Already in Use

**Problem**: `uvicorn` says port 8000 is already in use.

**Solution**:

**Option 1**: Use a different port
```bash
uvicorn api.index:app --reload --port 8001
```

**Option 2**: Find and kill the process using port 8000
```bash
# On Unix/macOS:
lsof -ti:8000 | xargs kill -9

# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

### 🔴 Playground Not Loading

**Problem**: `/playground` returns 404 or doesn't work.

**Solution**:

1. **Check file exists**
   ```bash
   ls pages/playground.html
   ```

2. **Restart server**
   ```bash
   # Stop server (Ctrl+C)
   # Start again
   uvicorn api.index:app --reload
   ```

3. **Check URL**
   - Correct: `http://localhost:8000/playground`
   - Not: `http://localhost:8000/playground/`

---

### 🔴 Permission Denied (setup scripts)

**Problem**: Cannot execute `./setup.sh`.

**Solution**:
```bash
# Make script executable
chmod +x setup.sh

# Then run it
./setup.sh
```

---

## First-Time Contributors

Welcome! We're excited to have you contribute to Savrli AI. Here's how to get started:

### Finding Your First Issue

Look for issues labeled **"First Issue"** in our [GitHub Issues](https://github.com/Savrli-Inc/Savrli-AI/issues?q=is%3Aissue+is%3Aopen+label%3A%22First+Issue%22):

These issues are:
- ✅ Well-documented with clear requirements
- ✅ Good for beginners to learn the codebase
- ✅ Usually smaller in scope
- ✅ Have mentorship available

### Contribution Workflow

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes**
5. **Run tests**
   ```bash
   pytest tests/ -v
   ```
6. **Commit with clear message**
   ```bash
   git commit -m "feat: add your feature description"
   ```
7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
8. **Open a Pull Request** from your fork to our main repository

### Beginner-Friendly Areas

**Documentation** 📚
- Improve README clarity
- Add code examples
- Fix typos or outdated info
- Write tutorials

**Testing** 🧪
- Add test cases
- Improve test coverage
- Add edge case tests

**Small Features** ⚡
- Add parameter validation
- Improve error messages
- Add helpful logging

**Bug Fixes** 🐛
- Fix issues labeled "good first issue"
- Improve error handling

### Getting Help

- 💬 **Questions**: Open a [Discussion](https://github.com/Savrli-Inc/Savrli-AI/discussions)
- 🐛 **Bugs**: Open an [Issue](https://github.com/Savrli-Inc/Savrli-AI/issues)
- 📖 **Documentation**: Check [CONTRIBUTING.md](../CONTRIBUTING.md)
- 🤝 **Community**: Join our community channels

### Tips for Success

1. **Start Small**: Don't try to tackle everything at once
2. **Ask Questions**: No question is too simple
3. **Read the Code**: Understanding existing patterns helps
4. **Test Thoroughly**: Run tests before submitting
5. **Follow Style Guide**: Consistency matters
6. **Be Patient**: Reviews may take time

---

## Learning Resources

### Python & FastAPI

- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Real Python Tutorials](https://realpython.com/)

### OpenAI API

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [OpenAI Cookbook](https://cookbook.openai.com/)
- [GPT Best Practices](https://platform.openai.com/docs/guides/gpt-best-practices)

### Testing

- [Pytest Documentation](https://docs.pytest.org/)
- [Testing FastAPI](https://fastapi.tiangolo.com/tutorial/testing/)

### Git & GitHub

- [GitHub Skills](https://skills.github.com/)
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [How to Write Good Commit Messages](https://chris.beams.io/posts/git-commit/)

### Project-Specific

- [README.md](../README.md) - Full API documentation
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [docs/INTEGRATION_API.md](INTEGRATION_API.md) - Integration API docs
- [docs/PLUGIN_EXAMPLES.md](PLUGIN_EXAMPLES.md) - Plugin examples

---

## Need More Help?

- 📧 **Email**: Contact the maintainers
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Savrli-Inc/Savrli-AI/discussions)
- 🐛 **Issues**: [GitHub Issues](https://github.com/Savrli-Inc/Savrli-AI/issues)
- 📖 **Docs**: [Full Documentation](../README.md)

---

**Happy Coding! Welcome to the Savrli AI community! 🎉**
