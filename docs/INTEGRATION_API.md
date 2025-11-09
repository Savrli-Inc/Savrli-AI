# Integration API Documentation

## Overview

Savrli AI provides a plugin-based architecture for integrating with popular productivity platforms. This documentation covers the integration endpoints and provides examples for extending the system with custom plugins.

## Table of Contents

1. [Supported Platforms](#supported-platforms)
2. [Plugin Architecture](#plugin-architecture)
3. [API Endpoints](#api-endpoints)
4. [Integration Examples](#integration-examples)
5. [Third-Party Extension Guide](#third-party-extension-guide)
6. [Environment Configuration](#environment-configuration)

---

## Supported Platforms

Savrli AI currently supports integration with the following platforms:

- **Slack** - Send messages, process events, handle slash commands
- **Discord** - Send messages, process interactions, handle webhooks
- **Notion** - Create/update pages, manage databases
- **Google Docs** - Create/update documents, format text

---

## Plugin Architecture

### Core Concepts

The plugin system is built on three main components:

1. **Plugin Base Class** - Abstract interface that all plugins must implement
2. **Plugin Manager** - Manages plugin lifecycle and routing
3. **Platform Plugins** - Specific implementations for each platform

### Plugin Interface

All plugins must implement the following methods:

```python
class Plugin(ABC):
    def send_message(self, channel: str, message: str, **kwargs) -> Dict[str, Any]:
        """Send a message to the platform"""
        pass
    
    def process_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming webhook from platform"""
        pass
    
    def validate_config(self) -> bool:
        """Validate plugin configuration"""
        pass
```

---

## API Endpoints

### Base URL

```
Production: https://your-deployment.vercel.app
Local: http://localhost:8000
```

### 1. List Integrations

Get all available integration plugins and their status.

**Endpoint:** `GET /integrations`

**Response:**
```json
{
  "integrations": [
    {
      "name": "slack",
      "enabled": true,
      "class": "SlackPlugin"
    },
    {
      "name": "discord",
      "enabled": true,
      "class": "DiscordPlugin"
    }
  ],
  "count": 2
}
```

**Example:**
```bash
curl https://your-api-url/integrations
```

---

### 2. Send Message via Integration

Send a message through a specific integration plugin.

**Endpoint:** `POST /integrations/send`

**Request Body:**
```json
{
  "plugin": "slack",
  "channel": "C1234567890",
  "message": "Hello from Savrli AI!",
  "metadata": {
    "thread_ts": "1234567890.123456"
  }
}
```

**Response:**
```json
{
  "success": true,
  "plugin": "slack",
  "result": {
    "status": "success",
    "channel": "C1234567890",
    "message": "Hello from Savrli AI!"
  }
}
```

**Example:**
```bash
curl -X POST https://your-api-url/integrations/send \
  -H "Content-Type: application/json" \
  -d '{
    "plugin": "slack",
    "channel": "C1234567890",
    "message": "Hello from Savrli AI!"
  }'
```

---

### 3. Process Webhook

Process incoming webhooks from integration platforms.

**Endpoint:** `POST /integrations/webhook`

**Request Body:**
```json
{
  "plugin": "slack",
  "data": {
    "type": "event_callback",
    "event": {
      "type": "message",
      "text": "Hello bot",
      "channel": "C1234567890",
      "user": "U1234567890"
    }
  }
}
```

**Response:**
```json
{
  "success": true,
  "plugin": "slack",
  "result": {
    "status": "success",
    "event_type": "message",
    "processed": true
  }
}
```

---

### 4. Get Integration Info

Get detailed information about a specific integration.

**Endpoint:** `GET /integrations/{plugin_name}/info`

**Response:**
```json
{
  "plugin": "SlackPlugin",
  "endpoints": {
    "send_message": "/integrations/slack/send",
    "webhook": "/integrations/slack/webhook"
  },
  "required_scopes": [
    "chat:write",
    "channels:read"
  ],
  "documentation": "https://api.slack.com/docs"
}
```

**Example:**
```bash
curl https://your-api-url/integrations/slack/info
```

---

## Platform-Specific Endpoints

### Slack

#### Send Message
**Endpoint:** `POST /integrations/slack/send`

**Parameters:**
- `channel` (string, required) - Channel ID or name
- `message` (string, required) - Message text
- `thread_ts` (string, optional) - Thread timestamp for replies

**Example:**
```bash
curl -X POST https://your-api-url/integrations/slack/send \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "#general",
    "message": "Hello from Savrli AI!",
    "thread_ts": "1234567890.123456"
  }'
```

---

### Discord

#### Send Message
**Endpoint:** `POST /integrations/discord/send`

**Parameters:**
- `channel` (string, required) - Channel ID
- `message` (string, required) - Message text
- `embed` (object, optional) - Rich embed object

**Example:**
```bash
curl -X POST https://your-api-url/integrations/discord/send \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "123456789012345678",
    "message": "Hello from Savrli AI!",
    "embed": {
      "title": "AI Response",
      "description": "Here is your answer",
      "color": 5814783
    }
  }'
```

---

### Notion

#### Create Page
**Endpoint:** `POST /integrations/notion/create`

**Parameters:**
- `page_id` (string, required) - Parent page or database ID
- `content` (string, required) - Page content
- `properties` (object, optional) - Page properties

**Example:**
```bash
curl -X POST https://your-api-url/integrations/notion/create \
  -H "Content-Type: application/json" \
  -d '{
    "page_id": "abc123-def456-ghi789",
    "content": "AI-generated content here",
    "properties": {
      "title": "New AI Page",
      "tags": ["ai", "automation"]
    }
  }'
```

---

### Google Docs

#### Create Document
**Endpoint:** `POST /integrations/google-docs/create`

**Parameters:**
- `title` (string, required) - Document title
- `content` (string, required) - Initial content

**Example:**
```bash
curl -X POST https://your-api-url/integrations/google-docs/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "AI Generated Document",
    "content": "This is AI-generated content."
  }'
```

#### Append Text
**Endpoint:** `POST /integrations/google-docs/append`

**Parameters:**
- `document_id` (string, required) - Document ID
- `content` (string, required) - Text to append
- `index` (integer, optional) - Insert position

**Example:**
```bash
curl -X POST https://your-api-url/integrations/google-docs/append \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "1abc-2def-3ghi",
    "content": "Additional content from AI",
    "index": 1
  }'
```

---

## Integration Examples

### Example 1: AI-Powered Slack Bot

```python
import requests

# Configure AI chat request
ai_request = {
    "prompt": "Generate a daily standup summary",
    "system": "You are a helpful project management assistant.",
    "session_id": "team-standup"
}

# Get AI response
ai_response = requests.post(
    "https://your-api-url/ai/chat",
    json=ai_request
).json()

# Send to Slack
slack_request = {
    "plugin": "slack",
    "channel": "#daily-standup",
    "message": ai_response["response"]
}

result = requests.post(
    "https://your-api-url/integrations/send",
    json=slack_request
).json()

print(result)
```

### Example 2: Discord Command Handler

```python
# Process Discord slash command
webhook_data = {
    "plugin": "discord",
    "data": {
        "type": 2,  # APPLICATION_COMMAND
        "data": {
            "name": "ask",
            "options": [
                {
                    "name": "question",
                    "value": "What is machine learning?"
                }
            ]
        }
    }
}

# Process webhook (this would trigger AI response)
result = requests.post(
    "https://your-api-url/integrations/webhook",
    json=webhook_data
).json()
```

### Example 3: Notion Page Creation

```python
# Generate content with AI
ai_response = requests.post(
    "https://your-api-url/ai/chat",
    json={
        "prompt": "Write a project plan for building a mobile app",
        "max_tokens": 1500
    }
).json()

# Create Notion page
notion_request = {
    "page_id": "parent-page-id",
    "content": ai_response["response"],
    "properties": {
        "title": "AI-Generated Project Plan",
        "status": "Draft"
    }
}

result = requests.post(
    "https://your-api-url/integrations/notion/create",
    json=notion_request
).json()
```

### Example 4: Google Docs Generation

```python
# Generate document with AI
ai_response = requests.post(
    "https://your-api-url/ai/chat",
    json={
        "prompt": "Write a comprehensive guide on REST APIs",
        "max_tokens": 2000
    }
).json()

# Create Google Doc
gdocs_request = {
    "title": "REST API Guide",
    "content": ai_response["response"]
}

result = requests.post(
    "https://your-api-url/integrations/google-docs/create",
    json=gdocs_request
).json()
```

---

## Third-Party Extension Guide

### Creating a Custom Plugin

To create a custom integration plugin, follow these steps:

#### Step 1: Create Plugin Class

```python
from integrations.plugin_base import Plugin
from typing import Dict, Any, Optional

class CustomPlugin(Plugin):
    """Custom integration plugin"""
    
    def __init__(self, ai_system: Any, config: Optional[Dict[str, Any]] = None):
        super().__init__(ai_system, config)
        self.api_key = self.config.get("api_key")
    
    def validate_config(self) -> bool:
        """Validate configuration"""
        return self.api_key is not None
    
    def send_message(self, channel: str, message: str, **kwargs) -> Dict[str, Any]:
        """Send message to platform"""
        # Implement your platform-specific logic here
        return {
            "status": "success",
            "channel": channel,
            "message": message
        }
    
    def process_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming webhook"""
        # Implement your webhook handling logic here
        return {
            "status": "success",
            "processed": True
        }
```

#### Step 2: Register Plugin

```python
from integrations.plugin_base import PluginManager
from custom_plugin import CustomPlugin

# Initialize plugin manager
manager = PluginManager(ai_system=client)

# Create and register plugin
config = {"api_key": "your-api-key"}
custom_plugin = CustomPlugin(ai_system=client, config=config)
manager.register_plugin("custom", custom_plugin)
```

#### Step 3: Use Plugin

```python
# Send message via custom plugin
result = manager.send_message(
    plugin_name="custom",
    channel="channel-id",
    message="Hello from custom plugin!"
)

# Process webhook
result = manager.process_webhook(
    plugin_name="custom",
    webhook_data={"type": "event", "data": {...}}
)
```

### Plugin Best Practices

1. **Error Handling** - Always wrap external API calls in try-except blocks
2. **Validation** - Validate all inputs before processing
3. **Logging** - Use Python logging module for debugging
4. **Configuration** - Store sensitive data in environment variables
5. **Documentation** - Implement `get_api_info()` method with clear documentation
6. **Testing** - Write comprehensive unit tests for your plugin

---

## Environment Configuration

### Required Environment Variables

For the core AI functionality:
```bash
OPENAI_API_KEY=your-openai-api-key
```

### Integration-Specific Variables

#### Slack
```bash
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret
SLACK_ENABLED=true
```

#### Discord
```bash
DISCORD_BOT_TOKEN=your-bot-token
DISCORD_APP_ID=your-application-id
DISCORD_PUBLIC_KEY=your-public-key
DISCORD_ENABLED=true
```

#### Notion
```bash
NOTION_API_TOKEN=secret_your-notion-integration-token
NOTION_ENABLED=true
```

#### Google Docs
```bash
GOOGLE_DOCS_CREDENTIALS=your-service-account-json
GOOGLE_DOCS_ENABLED=true
```

### Example .env File

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

## Error Handling

All endpoints return standard error responses:

**400 Bad Request** - Invalid parameters or plugin disabled
```json
{
  "detail": "Plugin slack is disabled"
}
```

**404 Not Found** - Plugin not found
```json
{
  "detail": "Plugin unknown not found"
}
```

**503 Service Unavailable** - External service error
```json
{
  "detail": "AI temporarily unavailable"
}
```

---

## Rate Limits

Rate limits depend on the specific platform:

- **Slack**: Tier-based rate limits (typically 1+ request per second)
- **Discord**: 50 requests per second per account
- **Notion**: 3 requests per second
- **Google Docs**: 100 requests per 100 seconds per user

---

## Support and Documentation

- **Main README**: `/README.md`
- **API Documentation**: `/docs/INTEGRATION_API.md` (this file)
- **Plugin Examples**: `/docs/PLUGIN_EXAMPLES.md`
- **Issues**: [GitHub Issues](https://github.com/Savrli-Inc/Savrli-AI/issues)

---

**Last Updated:** 2025-11-09
