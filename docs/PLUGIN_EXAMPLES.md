# Plugin Integration Examples

This document provides practical examples for integrating Savrli AI with various productivity platforms.

## Table of Contents

1. [Slack Examples](#slack-examples)
2. [Discord Examples](#discord-examples)
3. [Notion Examples](#notion-examples)
4. [Google Docs Examples](#google-docs-examples)
5. [Combined Workflows](#combined-workflows)

---

## Slack Examples

### Example 1: AI-Powered Q&A Bot

Create a Slack bot that answers questions using Savrli AI.

```python
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
API_URL = "https://your-savrli-deployment.vercel.app"

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json
    
    # Handle URL verification
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data["challenge"]})
    
    # Handle message events
    if data.get("type") == "event_callback":
        event = data.get("event", {})
        
        if event.get("type") == "app_mention":
            user_message = event.get("text", "")
            channel = event.get("channel")
            
            # Get AI response
            ai_response = requests.post(
                f"{API_URL}/ai/chat",
                json={
                    "prompt": user_message,
                    "system": "You are a helpful Slack assistant.",
                    "session_id": f"slack-{channel}"
                }
            ).json()
            
            # Send response to Slack
            requests.post(
                f"{API_URL}/integrations/slack/send",
                json={
                    "channel": channel,
                    "message": ai_response["response"]
                }
            )
    
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(port=3000)
```

### Example 2: Daily Standup Summarizer

Automatically summarize daily standup messages.

```python
import requests
from datetime import datetime

API_URL = "https://your-savrli-deployment.vercel.app"

def summarize_standup(channel_id, messages):
    """Summarize standup messages for a team"""
    
    # Combine all standup messages
    combined = "\n".join([f"- {msg}" for msg in messages])
    
    # Get AI summary
    prompt = f"""Summarize the following standup updates:
    
{combined}

Provide a concise summary highlighting:
1. Key accomplishments
2. Blockers or issues
3. Planned work
"""
    
    ai_response = requests.post(
        f"{API_URL}/ai/chat",
        json={
            "prompt": prompt,
            "system": "You are a project management assistant.",
            "max_tokens": 500
        }
    ).json()
    
    # Post summary to Slack
    requests.post(
        f"{API_URL}/integrations/slack/send",
        json={
            "channel": channel_id,
            "message": f"📊 *Daily Standup Summary*\n\n{ai_response['response']}"
        }
    )

# Usage
standup_messages = [
    "Completed the user authentication feature",
    "Working on database optimization - blocked by server access",
    "Will start on the API documentation today"
]

summarize_standup("#engineering", standup_messages)
```

### Example 3: Code Review Assistant

Help with code reviews in Slack.

```python
import requests

API_URL = "https://your-savrli-deployment.vercel.app"

def review_code_snippet(channel_id, code, language="python"):
    """Review code snippet and provide feedback"""
    
    prompt = f"""Review this {language} code and provide:
1. Potential bugs or issues
2. Performance suggestions
3. Best practice recommendations

Code:
```{language}
{code}
```
"""
    
    ai_response = requests.post(
        f"{API_URL}/ai/chat",
        json={
            "prompt": prompt,
            "system": "You are an experienced code reviewer.",
            "max_tokens": 800
        }
    ).json()
    
    requests.post(
        f"{API_URL}/integrations/slack/send",
        json={
            "channel": channel_id,
            "message": f"🔍 *Code Review*\n\n{ai_response['response']}"
        }
    )

# Usage
code = """
def process_data(data):
    result = []
    for item in data:
        result.append(item * 2)
    return result
"""

review_code_snippet("#code-reviews", code, "python")
```

---

## Discord Examples

### Example 1: Slash Command Handler

Implement AI-powered slash commands in Discord.

```python
import requests
from flask import Flask, request, jsonify
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

app = Flask(__name__)
API_URL = "https://your-savrli-deployment.vercel.app"
PUBLIC_KEY = "your-discord-public-key"

verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

@app.route("/discord/interactions", methods=["POST"])
def discord_interactions():
    # Verify Discord signature
    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")
    body = request.data.decode("utf-8")
    
    try:
        verify_key.verify(f"{timestamp}{body}".encode(), bytes.fromhex(signature))
    except BadSignatureError:
        return "Invalid signature", 401
    
    data = request.json
    
    # Handle PING
    if data["type"] == 1:
        return jsonify({"type": 1})
    
    # Handle APPLICATION_COMMAND
    if data["type"] == 2:
        command = data["data"]["name"]
        
        if command == "ask":
            question = data["data"]["options"][0]["value"]
            
            # Get AI response
            ai_response = requests.post(
                f"{API_URL}/ai/chat",
                json={
                    "prompt": question,
                    "system": "You are a helpful Discord assistant.",
                    "max_tokens": 500
                }
            ).json()
            
            return jsonify({
                "type": 4,
                "data": {
                    "content": ai_response["response"]
                }
            })
    
    return jsonify({"type": 4, "data": {"content": "Unknown command"}})

if __name__ == "__main__":
    app.run(port=3001)
```

### Example 2: Auto-Moderation Bot

Moderate Discord messages using AI.

```python
import requests

API_URL = "https://your-savrli-deployment.vercel.app"

def moderate_message(message_content, channel_id):
    """Check if message violates community guidelines"""
    
    prompt = f"""Analyze this message for:
1. Inappropriate language
2. Spam content
3. Violations of community guidelines

Message: "{message_content}"

Respond with:
- Status: APPROVED or FLAGGED
- Reason: Brief explanation
- Confidence: 0-100%
"""
    
    ai_response = requests.post(
        f"{API_URL}/ai/chat",
        json={
            "prompt": prompt,
            "system": "You are a content moderation assistant.",
            "temperature": 0.3
        }
    ).json()
    
    # Parse response and take action
    response_text = ai_response["response"]
    
    if "FLAGGED" in response_text:
        # Send warning to channel
        requests.post(
            f"{API_URL}/integrations/discord/send",
            json={
                "channel": channel_id,
                "message": "⚠️ This message has been flagged for review.",
                "embed": {
                    "title": "Moderation Alert",
                    "description": response_text,
                    "color": 16711680  # Red
                }
            }
        )
    
    return response_text

# Usage
moderate_message("Sample message content", "123456789012345678")
```

---

## Notion Examples

### Example 1: Meeting Notes Generator

Automatically generate meeting notes in Notion.

```python
import requests
from datetime import datetime

API_URL = "https://your-savrli-deployment.vercel.app"

def create_meeting_notes(page_id, participants, topics):
    """Generate and save meeting notes to Notion"""
    
    prompt = f"""Generate professional meeting notes for:

Date: {datetime.now().strftime("%Y-%m-%d")}
Participants: {', '.join(participants)}
Topics: {', '.join(topics)}

Include:
1. Meeting summary
2. Key discussion points
3. Action items
4. Next steps
"""
    
    ai_response = requests.post(
        f"{API_URL}/ai/chat",
        json={
            "prompt": prompt,
            "system": "You are a professional meeting note-taker.",
            "max_tokens": 1000
        }
    ).json()
    
    # Create Notion page
    result = requests.post(
        f"{API_URL}/integrations/notion/create",
        json={
            "page_id": page_id,
            "content": ai_response["response"],
            "properties": {
                "title": f"Meeting Notes - {datetime.now().strftime('%Y-%m-%d')}",
                "date": datetime.now().isoformat(),
                "participants": participants
            }
        }
    ).json()
    
    return result

# Usage
create_meeting_notes(
    page_id="parent-page-id",
    participants=["Alice", "Bob", "Charlie"],
    topics=["Q4 Planning", "Budget Review", "Team Updates"]
)
```

### Example 2: Project Documentation Generator

Generate project documentation from prompts.

```python
import requests

API_URL = "https://your-savrli-deployment.vercel.app"

def generate_project_docs(database_id, project_name, description):
    """Generate comprehensive project documentation"""
    
    sections = [
        "Project Overview",
        "Technical Architecture",
        "Implementation Plan",
        "Testing Strategy",
        "Deployment Guide"
    ]
    
    full_content = []
    
    for section in sections:
        prompt = f"""Create a detailed {section} section for:

Project: {project_name}
Description: {description}

Provide professional, comprehensive content suitable for technical documentation.
"""
        
        ai_response = requests.post(
            f"{API_URL}/ai/chat",
            json={
                "prompt": prompt,
                "system": "You are a technical documentation expert.",
                "max_tokens": 1500
            }
        ).json()
        
        full_content.append(f"## {section}\n\n{ai_response['response']}\n\n")
    
    # Create Notion page
    result = requests.post(
        f"{API_URL}/integrations/notion/create",
        json={
            "page_id": database_id,
            "content": "\n".join(full_content),
            "properties": {
                "title": f"{project_name} Documentation",
                "status": "Draft",
                "type": "Documentation"
            }
        }
    ).json()
    
    return result

# Usage
generate_project_docs(
    database_id="database-id",
    project_name="Mobile App Redesign",
    description="Complete redesign of the mobile application with new UI/UX"
)
```

---

## Google Docs Examples

### Example 1: Report Generator

Generate formatted reports in Google Docs.

```python
import requests

API_URL = "https://your-savrli-deployment.vercel.app"

def generate_monthly_report(data):
    """Generate monthly performance report"""
    
    prompt = f"""Create a professional monthly performance report with:

Metrics:
- Revenue: ${data['revenue']:,}
- Users: {data['users']:,}
- Growth: {data['growth']}%

Analyze trends and provide:
1. Executive Summary
2. Key Achievements
3. Challenges
4. Recommendations for next month
"""
    
    ai_response = requests.post(
        f"{API_URL}/ai/chat",
        json={
            "prompt": prompt,
            "system": "You are a business analyst.",
            "max_tokens": 2000
        }
    ).json()
    
    # Create Google Doc
    result = requests.post(
        f"{API_URL}/integrations/google-docs/create",
        json={
            "title": f"Monthly Report - {data['month']}",
            "content": ai_response["response"]
        }
    ).json()
    
    return result

# Usage
report_data = {
    "month": "November 2025",
    "revenue": 125000,
    "users": 5400,
    "growth": 15.3
}

generate_monthly_report(report_data)
```

### Example 2: Collaborative Document Updater

Append AI-generated content to existing documents.

```python
import requests

API_URL = "https://your-savrli-deployment.vercel.app"

def add_section_to_doc(doc_id, section_title, topic):
    """Add AI-generated section to existing document"""
    
    prompt = f"""Write a comprehensive section titled "{section_title}" about:

{topic}

Provide detailed, well-structured content with:
- Clear explanations
- Examples where relevant
- Best practices
"""
    
    ai_response = requests.post(
        f"{API_URL}/ai/chat",
        json={
            "prompt": prompt,
            "system": "You are a technical writer.",
            "max_tokens": 1500
        }
    ).json()
    
    # Append to Google Doc
    content = f"\n\n## {section_title}\n\n{ai_response['response']}\n"
    
    result = requests.post(
        f"{API_URL}/integrations/google-docs/append",
        json={
            "document_id": doc_id,
            "content": content
        }
    ).json()
    
    return result

# Usage
add_section_to_doc(
    doc_id="existing-doc-id",
    section_title="API Security",
    topic="Best practices for securing REST APIs including authentication, rate limiting, and data validation"
)
```

---

## Combined Workflows

### Workflow 1: Multi-Platform Announcement

Send AI-enhanced announcements to multiple platforms.

```python
import requests

API_URL = "https://your-savrli-deployment.vercel.app"

def broadcast_announcement(announcement, platforms):
    """Send announcement to multiple platforms"""
    
    # Optimize message for each platform
    results = {}
    
    for platform in platforms:
        prompt = f"""Adapt this announcement for {platform}:

{announcement}

Make it platform-appropriate while preserving the core message.
Platform-specific guidelines:
- Slack: Professional, concise, use emojis sparingly
- Discord: Casual, engaging, can use more emojis
- Notion: Formal, detailed, structured
"""
        
        ai_response = requests.post(
            f"{API_URL}/ai/chat",
            json={
                "prompt": prompt,
                "max_tokens": 300
            }
        ).json()
        
        optimized_message = ai_response["response"]
        
        # Send to platform
        if platform == "slack":
            result = requests.post(
                f"{API_URL}/integrations/slack/send",
                json={
                    "channel": "#announcements",
                    "message": optimized_message
                }
            ).json()
        
        elif platform == "discord":
            result = requests.post(
                f"{API_URL}/integrations/discord/send",
                json={
                    "channel": "announcements-channel-id",
                    "message": optimized_message
                }
            ).json()
        
        elif platform == "notion":
            result = requests.post(
                f"{API_URL}/integrations/notion/create",
                json={
                    "page_id": "announcements-page-id",
                    "content": optimized_message,
                    "properties": {"title": "New Announcement"}
                }
            ).json()
        
        results[platform] = result
    
    return results

# Usage
announcement = "We're launching our new mobile app next week! Get ready for improved performance and new features."
broadcast_announcement(announcement, ["slack", "discord", "notion"])
```

### Workflow 2: Knowledge Base Sync

Sync Q&A across platforms using AI.

```python
import requests

API_URL = "https://your-savrli-deployment.vercel.app"

def sync_knowledge_base(question, answer):
    """Create knowledge base entry across platforms"""
    
    # Format for Slack (pinned message)
    slack_format = f"*Q: {question}*\nA: {answer}"
    
    # Format for Notion (structured page)
    notion_format = f"# {question}\n\n{answer}"
    
    # Format for Google Docs (FAQ section)
    docs_format = f"**Q: {question}**\n\n{answer}\n\n---\n"
    
    results = {
        "slack": requests.post(
            f"{API_URL}/integrations/slack/send",
            json={
                "channel": "#faq",
                "message": slack_format
            }
        ).json(),
        
        "notion": requests.post(
            f"{API_URL}/integrations/notion/create",
            json={
                "page_id": "faq-database-id",
                "content": notion_format,
                "properties": {
                    "title": question,
                    "category": "FAQ"
                }
            }
        ).json(),
        
        "google_docs": requests.post(
            f"{API_URL}/integrations/google-docs/append",
            json={
                "document_id": "faq-doc-id",
                "content": docs_format
            }
        ).json()
    }
    
    return results

# Usage
sync_knowledge_base(
    question="How do I reset my password?",
    answer="Click on 'Forgot Password' on the login page and follow the email instructions."
)
```

---

## Best Practices

1. **Error Handling**: Always wrap API calls in try-except blocks
2. **Rate Limiting**: Implement exponential backoff for retries
3. **Session Management**: Use session IDs for context-aware conversations
4. **Security**: Never hardcode API keys; use environment variables
5. **Testing**: Test integrations in a development environment first
6. **Monitoring**: Log all integration activities for debugging
7. **Fallbacks**: Implement fallback mechanisms for API failures

---

## Additional Resources

- [Integration API Documentation](INTEGRATION_API.md)
- [Savrli AI Main README](../README.md)
- [Platform-Specific SDKs](#platform-sdks)

### Platform SDKs

- **Slack**: [slack-sdk](https://github.com/slackapi/python-slack-sdk)
- **Discord**: [discord.py](https://github.com/Rapptz/discord.py)
- **Notion**: [notion-client](https://github.com/ramnes/notion-sdk-py)
- **Google Docs**: [google-api-python-client](https://github.com/googleapis/google-api-python-client)

---

**Last Updated:** 2025-11-09
