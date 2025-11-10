# Savrli AI Quickstart Guide

Get started with Savrli AI in minutes! This guide will walk you through the essential features and common use cases.

## Table of Contents

1. [Setup](#setup)
2. [Basic Chat](#basic-chat)
3. [Multi-Modal AI](#multi-modal-ai)
4. [AI Tools](#ai-tools)
5. [Dashboard](#dashboard)
6. [Integrations](#integrations)
7. [Next Steps](#next-steps)

---

## Setup

### 1. Clone and Install

```bash
git clone https://github.com/Savrli-Inc/Savrli-AI.git
cd Savrli-AI
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```bash
OPENAI_API_KEY=your-api-key-here
```

### 3. Run Locally

```bash
uvicorn api.index:app --reload
```

The API will be available at `http://localhost:8000`

---

## Basic Chat

### Simple Conversation

```bash
curl -X POST http://localhost:8000/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing in simple terms"
  }'
```

### With Conversation History

```bash
# First message
curl -X POST http://localhost:8000/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is Python?",
    "session_id": "my-session"
  }'

# Follow-up (AI remembers context)
curl -X POST http://localhost:8000/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What are its main features?",
    "session_id": "my-session"
  }'
```

### With Custom Behavior

```bash
curl -X POST http://localhost:8000/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Review this code",
    "system": "You are an expert Python developer who provides constructive code reviews.",
    "temperature": 0.3
  }'
```

---

## Multi-Modal AI

### List Available Models

```bash
curl http://localhost:8000/ai/models
```

### Analyze an Image

```bash
curl -X POST http://localhost:8000/ai/vision \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What objects are in this image?",
    "image_url": "https://example.com/image.jpg"
  }'
```

### Transcribe Audio

```bash
curl -X POST http://localhost:8000/ai/audio/transcribe \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://example.com/audio.mp3",
    "language": "en"
  }'
```

### Get Model Details

```bash
curl http://localhost:8000/ai/models/gpt-4
```

---

## AI Tools

### Text Summarization

```bash
curl -X POST http://localhost:8000/ai/tools/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Long article text here...",
    "style": "bullet_points",
    "max_length": 150
  }'
```

**Available styles:**
- `concise` - Brief summary
- `detailed` - Comprehensive summary
- `bullet_points` - Key points as bullets

### Sentiment Analysis

```bash
curl -X POST http://localhost:8000/ai/tools/sentiment \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I absolutely love this new feature!",
    "detailed": true
  }'
```

**Returns:**
- Sentiment: positive, negative, or neutral
- Score: 0-100
- Emotions: joy, anger, sadness, etc.
- Tone: formal, casual, friendly, etc.

### Email Drafting

```bash
curl -X POST http://localhost:8000/ai/tools/email/draft \
  -H "Content-Type: application/json" \
  -d '{
    "purpose": "Request a meeting to discuss Q4 strategy",
    "recipient": "Sarah (Marketing Director)",
    "tone": "professional",
    "length": "medium",
    "key_points": [
      "Review Q4 goals",
      "Discuss budget allocation",
      "Plan campaign schedule"
    ]
  }'
```

**Tone options:** `professional`, `casual`, `friendly`, `formal`  
**Length options:** `short`, `medium`, `long`

### Workflow Automation

```bash
curl -X POST http://localhost:8000/ai/tools/workflow/suggest \
  -H "Content-Type: application/json" \
  -d '{
    "task_description": "Set up CI/CD pipeline for React application",
    "constraints": ["Must use GitHub Actions", "Deploy to AWS"],
    "tools_available": ["GitHub", "AWS", "Docker", "Jest"]
  }'
```

### List All Tools

```bash
curl http://localhost:8000/ai/tools
```

---

## Dashboard

### Access the Dashboard

Open your browser and navigate to:

```
http://localhost:8000/dashboard
```

### Dashboard Features

1. **Theme Toggle** - Click the moon/sun icon to switch themes
2. **Real-Time Stats** - View live metrics for requests, models, and sessions
3. **Model Overview** - See all available models and their capabilities
4. **Usage Analytics** - Visual breakdown of tool usage
5. **Performance Metrics** - Monitor API health
6. **Integration Status** - Check platform connections

The dashboard auto-refreshes every 10 seconds to show the latest data.

---

## Integrations

### Slack Integration

```bash
# Send message to Slack
curl -X POST http://localhost:8000/integrations/slack/send \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "#general",
    "message": "Hello from Savrli AI!"
  }'
```

### Discord Integration

```bash
# Send message to Discord
curl -X POST http://localhost:8000/integrations/discord/send \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "channel-id-here",
    "message": "Hello from Savrli AI!"
  }'
```

### Notion Integration

```bash
# Create Notion page
curl -X POST http://localhost:8000/integrations/notion/create \
  -H "Content-Type: application/json" \
  -d '{
    "page_id": "parent-page-id",
    "content": "Your content here",
    "properties": {
      "title": "New Page Title"
    }
  }'
```

### Google Docs Integration

```bash
# Create Google Doc
curl -X POST http://localhost:8000/integrations/google-docs/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Document",
    "content": "Your content here"
  }'
```

### List All Integrations

```bash
curl http://localhost:8000/integrations
```

---

## Common Use Cases

### 1. Meeting Assistant

Summarize meeting notes and draft follow-up emails:

```bash
# Summarize notes
curl -X POST http://localhost:8000/ai/tools/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Meeting notes...",
    "style": "bullet_points"
  }'

# Draft follow-up email
curl -X POST http://localhost:8000/ai/tools/email/draft \
  -H "Content-Type: application/json" \
  -d '{
    "purpose": "Follow up on meeting action items",
    "tone": "professional"
  }'
```

### 2. Content Analysis

Analyze customer feedback sentiment:

```bash
curl -X POST http://localhost:8000/ai/tools/sentiment \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Customer feedback text...",
    "detailed": true
  }'
```

### 3. Code Review Assistant

Get AI-powered code review:

```bash
curl -X POST http://localhost:8000/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Review this Python function: def process_data(data): ...",
    "system": "You are an expert code reviewer. Focus on bugs, performance, and best practices."
  }'
```

### 4. Documentation Generator

Create documentation from code or descriptions:

```bash
curl -X POST http://localhost:8000/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Generate API documentation for: POST /users endpoint that creates a new user",
    "system": "You are a technical writer creating clear API documentation."
  }'
```

### 5. Task Planning

Get optimized workflows:

```bash
curl -X POST http://localhost:8000/ai/tools/workflow/suggest \
  -H "Content-Type: application/json" \
  -d '{
    "task_description": "Launch new product feature",
    "constraints": ["2 week deadline", "Small team"],
    "tools_available": ["Jira", "GitHub", "Slack"]
  }'
```

---

## Next Steps

### Learn More

- 📚 [Full README](../README.md) - Complete documentation
- 🗺️ [Roadmap](../ROADMAP.md) - Future features and timeline
- 🔌 [Plugin Examples](../docs/PLUGIN_EXAMPLES.md) - Integration examples
- 🤝 [Contributing](../CONTRIBUTING.md) - Contribution guidelines

### Advanced Features

- **Streaming Responses** - Real-time token streaming
- **Fine-Tuning** - Custom model training
- **Batch Processing** - Process multiple requests
- **Custom Plugins** - Build your own integrations

### Playground

Try the visual interface:

```
http://localhost:8000/playground
```

- No code required
- Interactive UI
- Test all features
- Experiment with parameters

### Get Help

- 🐛 [Report Issues](https://github.com/Savrli-Inc/Savrli-AI/issues)
- 💬 [Join Discussions](https://github.com/Savrli-Inc/Savrli-AI/discussions)
- 📖 [View Examples](../docs/PLUGIN_EXAMPLES.md)

---

## Tips & Best Practices

### 1. Use Session IDs

Maintain context across multiple messages:

```bash
session_id="user-123-$(date +%s)"
```

### 2. Customize AI Behavior

Use system instructions for specialized tasks:

```json
{
  "system": "You are a [role]. Your expertise is [domain]."
}
```

### 3. Optimize Token Usage

- Use appropriate `max_tokens` for your needs
- Lower `temperature` for consistent outputs
- Higher `temperature` for creative outputs

### 4. Error Handling

Always check response status:

```bash
response=$(curl -s -w "\n%{http_code}" ...)
http_code=$(echo "$response" | tail -1)
body=$(echo "$response" | head -n -1)
```

### 5. Rate Limiting

Implement retry logic with exponential backoff for production use.

---

## Quick Reference Card

| Task | Endpoint | Method |
|------|----------|--------|
| Chat | `/ai/chat` | POST |
| List Models | `/ai/models` | GET |
| Vision Analysis | `/ai/vision` | POST |
| Audio Transcribe | `/ai/audio/transcribe` | POST |
| Summarize | `/ai/tools/summarize` | POST |
| Sentiment | `/ai/tools/sentiment` | POST |
| Email Draft | `/ai/tools/email/draft` | POST |
| Workflow | `/ai/tools/workflow/suggest` | POST |
| Dashboard | `/dashboard` | GET |
| Playground | `/playground` | GET |
| List Tools | `/ai/tools` | GET |
| Integrations | `/integrations` | GET |

---

**Happy Building! 🚀**

For questions or support, visit our [GitHub repository](https://github.com/Savrli-Inc/Savrli-AI).
