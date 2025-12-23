# Savrli AI Onboarding Guide

Welcome to Savrli AI! 🚀 This guide will help you get up and running quickly as a new contributor.

## Table of Contents

- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Automated Setup (Recommended)](#automated-setup-recommended)
- [Manual Setup](#manual-setup)
- [Verifying Your Setup](#verifying-your-setup)
- [Common Environment Variables](#common-environment-variables)
- [Troubleshooting](#troubleshooting)
- [First Contribution](#first-contribution)
- [Getting Help](#getting-help)

---

## Quick Start

**TL;DR - Get started in 3 commands:**

```bash
# 1. Clone the repository
git clone https://github.com/Savrli-Inc/Savrli-AI.git
cd Savrli-AI

# 2. Run the setup script
./scripts/setup.sh

# 3. Start the server
uvicorn api.index:app --reload
```

Then open `http://localhost:8000/playground` in your browser! 🎉

---

## Prerequisites

Before you begin, ensure you have the following installed:

### Required

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
  ```bash
  # Check your version
  python3 --version
  ```

- **pip** - Python package installer (usually included with Python)
  ```bash
  # Check if pip is installed
  python3 -m pip --version
  ```

- **Git** - Version control system
  ```bash
  # Check if git is installed
  git --version
  ```

### Recommended

- **Virtual environment tools** - `venv` (included with Python 3.8+)
- **Text editor or IDE** - VS Code, PyCharm, Sublime Text, etc.
- **Terminal/Command line** - Comfort with basic command line usage

### API Keys

- **OpenAI API Key** (Required) - Get one at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
  - You'll need this to run the AI features
  - Free tier available for testing
  - See [OpenAI Pricing](https://openai.com/pricing) for details

---

## Automated Setup (Recommended)

We provide an interactive setup script that handles everything for you.

### Running the Setup Script

```bash
# Navigate to the project directory
cd Savrli-AI

# Run the setup script
./scripts/setup.sh
```

### What the Script Does

The setup script will:

1. ✅ **Check Python version** - Ensures you have Python 3.8+
2. ✅ **Create virtual environment** - Asks if you want to create an isolated Python environment (recommended)
3. ✅ **Install dependencies** - Installs all required packages from `requirements.txt`
4. ✅ **Configure environment** - Helps you set up your `.env` file with API keys
5. ✅ **Run health checks** - Runs tests to verify everything works
6. ✅ **Show next steps** - Provides clear guidance on what to do next

### Interactive Prompts

The script will ask you questions like:

- **"Would you like to create a virtual environment?"** - Answer `y` (recommended)
- **"Would you like to configure .env now?"** - Answer `y` to set up your API key interactively
- **"Enter your OpenAI API key:"** - Paste your API key from OpenAI

### Script Features

- **Safe & Non-Destructive** - Won't delete files or overwrite without asking
- **Interactive** - Guides you through each step
- **Colorful Output** - Easy-to-read status messages
- **Error Handling** - Clear error messages and troubleshooting tips

---

## Manual Setup

If you prefer to set up manually or the script doesn't work:

### Step 1: Clone the Repository

```bash
git clone https://github.com/Savrli-Inc/Savrli-AI.git
cd Savrli-AI
```

### Step 2: Create Virtual Environment (Recommended)

A virtual environment keeps project dependencies isolated:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it (Unix/Linux/macOS)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate
```

**You'll see `(venv)` in your terminal prompt when activated.**

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**This installs:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `openai>=1.3.0` - OpenAI API client
- `pydantic` - Data validation
- `python-dotenv` - Environment variables
- `pytest` - Testing framework
- `httpx` - HTTP client for tests
- `python-multipart` - File upload support

### Step 4: Create Environment File

Create a `.env` file in the project root:

```bash
# Copy from example if it exists
cp .env.example .env

# Or create manually
touch .env
```

Add your configuration:

```bash
# REQUIRED - Get from https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-actual-api-key-here

# OPTIONAL (defaults shown, uncomment to customize)
# OPENAI_MODEL=gpt-3.5-turbo
# OPENAI_MAX_TOKENS=1000
# OPENAI_TEMPERATURE=0.7
# DEFAULT_CONTEXT_WINDOW=10
# MAX_HISTORY_PER_SESSION=20
```

**🔐 Security:** Never commit your `.env` file! It's already in `.gitignore`.

### Step 5: Verify Installation

Run the test suite:

```bash
python -m pytest tests/ -v
```

All tests should pass ✅

---

## Verifying Your Setup

### 1. Start the Development Server

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

### 2. Test with the Playground

Open your browser and navigate to:
```
http://localhost:8000/playground
```

**What you'll see:**
- Interactive chat interface
- Configuration panel (model, temperature, tokens)
- Multiple modes: Chat, Vision, Image Generation
- Real-time AI responses

**Try it out:**
1. Type a message like "Hello! Explain what this API does."
2. Click "Send"
3. Watch the AI response stream in real-time

### 3. Test with API Request

```bash
# Simple chat request
curl -X POST http://localhost:8000/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, how are you?"}'
```

**Expected response:**
```json
{
  "response": "Hello! I'm doing well, thank you for asking...",
  "session_id": "default",
  "timestamp": "2025-01-10T19:15:00.000000"
}
```

### 4. Run Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_api.py -v

# Run with coverage
python -m pytest --cov=api --cov=integrations tests/
```

---

## Common Environment Variables

Here's a comprehensive list of environment variables you can configure:

### Required Variables

```bash
# OpenAI API Key - REQUIRED for AI features
OPENAI_API_KEY=sk-your-api-key-here
```

### OpenAI Configuration

```bash
# Model to use (default: gpt-3.5-turbo)
OPENAI_MODEL=gpt-3.5-turbo
# Options: gpt-3.5-turbo, gpt-4, gpt-4-turbo-preview

# Maximum tokens in response (default: 1000)
OPENAI_MAX_TOKENS=1000
# Range: 1-2000 (higher values = longer responses, more cost)

# Response randomness (default: 0.7)
OPENAI_TEMPERATURE=0.7
# Range: 0.0-2.0 (0.0=deterministic, 2.0=very random)

# Number of conversation turns to keep (default: 10)
DEFAULT_CONTEXT_WINDOW=10
# Higher = better context, more API cost

# Maximum history entries per session (default: 20)
MAX_HISTORY_PER_SESSION=20
# Prevents memory leaks in long-running sessions
```

### Integration Platform Tokens (Optional)

```bash
# Slack Integration
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_SIGNING_SECRET=your-slack-signing-secret
SLACK_ENABLED=false

# Discord Integration
DISCORD_BOT_TOKEN=your-discord-bot-token
DISCORD_APP_ID=your-discord-app-id
DISCORD_PUBLIC_KEY=your-discord-public-key
DISCORD_ENABLED=false

# Notion Integration
NOTION_API_TOKEN=secret_your-notion-token
NOTION_ENABLED=false

# Google Docs Integration
GOOGLE_DOCS_CREDENTIALS=your-google-credentials-json
GOOGLE_DOCS_ENABLED=false
```

### Example .env File

```bash
# Core Configuration
OPENAI_API_KEY=sk-abc123...

# Custom Model Settings
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=1500
OPENAI_TEMPERATURE=0.8

# Enable Slack Integration
SLACK_BOT_TOKEN=xoxb-123...
SLACK_SIGNING_SECRET=abc123...
SLACK_ENABLED=true
```

---

## Troubleshooting

Common issues and how to fix them:

### 🔴 "OPENAI_API_KEY is not set"

**Problem:** The server won't start because the API key is missing.

**Solution:**
1. Check that `.env` file exists in project root
2. Open `.env` and verify: `OPENAI_API_KEY=sk-...`
3. Make sure there are no extra spaces: ❌ `OPENAI_API_KEY = sk-...` ✅ `OPENAI_API_KEY=sk-...`
4. Restart the server after editing `.env`

**Common mistakes:**
```bash
# Wrong - has quotes
OPENAI_API_KEY="sk-..."

# Wrong - has space
OPENAI_API_KEY = sk-...

# Correct
OPENAI_API_KEY=sk-...
```

---

### 🔴 "ModuleNotFoundError: No module named 'fastapi'"

**Problem:** Dependencies not installed or wrong Python environment.

**Solution:**

```bash
# Make sure you're in the project directory
cd Savrli-AI

# If using virtual environment, activate it
source venv/bin/activate  # Unix/Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

---

### 🔴 "Python version 3.7 detected, but 3.8+ is required"

**Problem:** Your Python version is too old.

**Solution:**

1. **Install Python 3.8+**
   - macOS: `brew install python@3.11`
   - Ubuntu/Debian: `sudo apt-get install python3.11`
   - Windows: Download from [python.org](https://www.python.org/downloads/)

2. **Use the new version**
   ```bash
   # Instead of python3, use specific version
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

---

### 🔴 "AI temporarily unavailable" (503 Error)

**Problem:** Can't reach OpenAI API.

**Possible causes:**

1. **Invalid API Key**
   - Check at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Make sure it's active and has quota

2. **Network Issues**
   - Check internet connection
   - Try accessing [platform.openai.com](https://platform.openai.com)

3. **Rate Limiting**
   - Wait a few minutes
   - Check OpenAI usage dashboard

4. **Quota Exceeded**
   - Log into OpenAI dashboard
   - Check usage and billing

---

### 🔴 Port Already in Use (8000)

**Problem:** `uvicorn` says port 8000 is occupied.

**Solution:**

**Option 1:** Use different port
```bash
uvicorn api.index:app --reload --port 8001
```

**Option 2:** Kill process on port 8000
```bash
# Unix/Linux/macOS
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

### 🔴 Tests Failing

**Problem:** `pytest` shows failing tests.

**Solutions:**

1. **Set test API key**
   ```bash
   export OPENAI_API_KEY=test-key-for-testing
   pytest tests/ -v
   ```

2. **Check Python version**
   ```bash
   python3 --version  # Should be 3.8+
   ```

3. **Reinstall dependencies**
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

4. **Run specific test to debug**
   ```bash
   pytest tests/test_api.py::TestChatRequestValidation -v
   ```

---

### 🔴 Virtual Environment Issues

**Problem:** Can't activate virtual environment.

**Solution:**

```bash
# Delete and recreate
rm -rf venv
python3 -m venv venv

# Activate (Unix/Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

### 🔴 Permission Denied (./scripts/setup.sh)

**Problem:** Can't execute setup script.

**Solution:**

```bash
# Make script executable
chmod +x scripts/setup.sh

# Run it
./scripts/setup.sh
```

---

## First Contribution

Ready to contribute? Here's how to get started:

### 1. Find a "First Issue"

Look for issues labeled **"First Issue"**: [View First Issues](https://github.com/Savrli-Inc/Savrli-AI/issues?q=is%3Aissue+is%3Aopen+label%3A%22First+Issue%22)

These issues are:
- ✅ Well-documented
- ✅ Beginner-friendly
- ✅ Smaller in scope
- ✅ Have mentor support

### 2. Claim an Issue

Comment on the issue:
```
Hi! I'd like to work on this issue. I've completed the setup following the onboarding guide.
```

### 3. Create a Branch

```bash
# Make sure you're on main
git checkout main

# Pull latest changes
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `test/` - Test additions

### 4. Make Your Changes

- Write clean, readable code
- Follow existing code style
- Add tests for new functionality
- Update documentation as needed

### 5. Test Your Changes

```bash
# Run tests
pytest tests/ -v

# Test manually
uvicorn api.index:app --reload
# Then test in playground or with curl
```

### 6. Commit Your Changes

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Good commit messages
git commit -m "feat: add temperature validation to chat endpoint"
git commit -m "fix: resolve session history memory leak"
git commit -m "docs: update API examples in README"
git commit -m "test: add tests for streaming responses"
```

### 7. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub!

### 8. Respond to Reviews

- Be open to feedback
- Make requested changes
- Ask questions if unclear
- Be patient - reviews take time

---

## Getting Help

### Resources

- 📖 **Documentation**
  - [README.md](../README.md) - Full API documentation
  - [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
  - [docs/INTEGRATION_API.md](INTEGRATION_API.md) - Integration development
  - [docs/PLUGIN_EXAMPLES.md](PLUGIN_EXAMPLES.md) - Plugin examples

- 💬 **Community**
  - [GitHub Discussions](https://github.com/Savrli-Inc/Savrli-AI/discussions) - Ask questions
  - [GitHub Issues](https://github.com/Savrli-Inc/Savrli-AI/issues) - Report bugs

### Before Asking for Help

1. **Check this guide** - The troubleshooting section covers common issues
2. **Search existing issues** - Your question might be answered
3. **Check the docs** - README and CONTRIBUTING have lots of info

### How to Ask for Help

**Good question:**
```
I'm getting a "ModuleNotFoundError: No module named 'fastapi'" error.

What I tried:
- Ran pip install -r requirements.txt
- Checked that I'm in the project directory
- Using Python 3.9

Here's the full error:
[paste error]
```

**Not helpful:**
```
It doesn't work, help!
```

---

## Next Steps

Now that you're set up:

1. ✅ **Explore the Playground** - `http://localhost:8000/playground`
2. ✅ **Read the API docs** - [README.md](../README.md)
3. ✅ **Try the examples** - Test different API endpoints
4. ✅ **Run the tests** - `pytest tests/ -v`
5. ✅ **Find a First Issue** - Start contributing!
6. ✅ **Join discussions** - Connect with the community

---

## Assumptions and References

### Assumptions Made by Setup Script

- Python 3.8+ is available on the system
- pip is installed and functional
- User has internet connectivity for package downloads
- User has write permissions in the project directory
- Virtual environment is created in `./venv` directory
- `.env` file can be created in project root

### References

For more detailed information, see:
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Full contribution guidelines, code style, testing requirements
- **[README.md](../README.md)** - Complete API documentation and examples
- **[docs/INTEGRATION_API.md](INTEGRATION_API.md)** - How to build integrations
- **Setup Script** - `scripts/setup.sh` for implementation details

---

**Welcome to Savrli AI! We're excited to have you here! 🎉**

If you have suggestions for improving this onboarding guide, please open an issue or PR!
