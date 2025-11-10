# Playground Integration Guide

This document describes how to integrate the Savrli AI interactive playground with multimodal endpoints.

## Overview

The playground provides a browser-based interface for testing AI capabilities with support for:
- Text chat completions
- Vision/image analysis
- Image generation (DALL-E)
- Session management
- Resource uploads (future)

## Architecture

### Frontend Components

1. **pages/playground.html** - Main UI with three modes:
   - Chat mode - Text-based conversations
   - Vision mode - Image analysis
   - Image Generation mode - DALL-E image creation

2. **static/js/playground.js** - JavaScript integration module with fetch-based API examples

### Backend Components

1. **api/playground.py** - FastAPI router for playground session management
2. **api/index.py** - Main application with mounted playground router

## API Endpoints

### Chat Endpoint

Send text prompts to the AI.

**Endpoint:** `POST /ai/chat`

**Request:**
```json
{
  "prompt": "Explain quantum computing in simple terms",
  "model": "gpt-3.5-turbo",
  "temperature": 0.7,
  "max_tokens": 1000,
  "session_id": "demo-session",
  "stream": false
}
```

**Response:**
```json
{
  "response": "Quantum computing is...",
  "session_id": "demo-session"
}
```

**curl Example:**
```bash
curl -X POST http://localhost:8000/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Hello, AI!",
    "model": "gpt-3.5-turbo",
    "temperature": 0.7
  }'
```

### Vision Endpoint

Analyze images with AI vision models.

**Endpoint:** `POST /ai/vision`

**Request:**
```json
{
  "prompt": "Describe this image in detail",
  "image_url": "https://example.com/image.jpg",
  "model": "gpt-4-vision-preview",
  "max_tokens": 300,
  "detail": "auto"
}
```

**Response:**
```json
{
  "response": "This image shows...",
  "model": "gpt-4-vision-preview"
}
```

**curl Example:**
```bash
curl -X POST http://localhost:8000/ai/vision \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What objects are in this image?",
    "image_url": "https://example.com/photo.jpg",
    "model": "gpt-4-vision-preview"
  }'
```

### Image Generation Endpoint

Generate images with DALL-E.

**Endpoint:** `POST /ai/image/generate`

**Request:**
```json
{
  "prompt": "A serene mountain landscape at sunset",
  "model": "dall-e-3",
  "size": "1024x1024",
  "quality": "standard",
  "n": 1
}
```

**Response:**
```json
{
  "images": [
    {
      "url": "https://...",
      "revised_prompt": "A serene mountain..."
    }
  ],
  "model": "dall-e-3",
  "count": 1
}
```

**curl Example:**
```bash
curl -X POST http://localhost:8000/ai/image/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A futuristic cityscape at night",
    "model": "dall-e-3",
    "size": "1024x1024",
    "quality": "hd"
  }'
```

### Playground Session Endpoints

#### Create Session

**Endpoint:** `POST /api/playground/session`

**Request:**
```json
{
  "name": "My Playground Session",
  "metadata": {
    "user": "demo_user",
    "project": "testing"
  }
}
```

**Response:**
```json
{
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "My Playground Session",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "message_count": 0,
  "metadata": {
    "user": "demo_user",
    "project": "testing"
  }
}
```

**curl Example:**
```bash
curl -X POST http://localhost:8000/api/playground/session \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Session",
    "metadata": {"user": "developer"}
  }'
```

#### Get Session

**Endpoint:** `GET /api/playground/session/{session_id}`

**curl Example:**
```bash
curl http://localhost:8000/api/playground/session/123e4567-e89b-12d3-a456-426614174000
```

#### Delete Session

**Endpoint:** `DELETE /api/playground/session/{session_id}`

**curl Example:**
```bash
curl -X DELETE http://localhost:8000/api/playground/session/123e4567-e89b-12d3-a456-426614174000
```

#### List Sessions

**Endpoint:** `GET /api/playground/sessions`

**Query Parameters:**
- `limit` - Maximum sessions to return (1-100, default 50)
- `offset` - Number of sessions to skip (default 0)

**curl Example:**
```bash
curl "http://localhost:8000/api/playground/sessions?limit=10&offset=0"
```

### Resource Upload Endpoint (Future)

Upload files for processing.

**Endpoint:** `POST /api/resources/upload` *(Stub for future implementation)*

**Request:**
```bash
# Multipart form data with file
```

**curl Example:**
```bash
curl -X POST http://localhost:8000/api/resources/upload \
  -F "file=@document.pdf" \
  -F "session_id=demo-session" \
  -F 'metadata={"type":"pdf","purpose":"analysis"}'
```

## JavaScript Integration

The `static/js/playground.js` file provides helper functions:

```javascript
// Chat example
const response = await callChatEndpoint("Hello!", {
  model: "gpt-3.5-turbo",
  temperature: 0.7,
  session_id: "my-session"
});
console.log(response.response);

// Session management example
const session = await createSession({
  name: "My Session"
});
const sessionInfo = await getSessionInfo(session.session_id);
await deleteSession(session.session_id);

// Upload example (future)
const fileInput = document.getElementById('fileInput');
const file = fileInput.files[0];
const uploadResponse = await uploadResource(file, {
  session_id: "my-session"
});
```

## Running the Playground

### Start the Server

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY=your-api-key-here

# Start the server
uvicorn api.index:app --reload
```

### Access the Playground

Navigate to: http://localhost:8000/playground

## Testing

Run the test suite:

```bash
# Run all tests
pytest tests/

# Run playground tests only
pytest tests/test_playground.py -v

# Run with coverage
pytest tests/test_playground.py --cov=api.playground
```

## Environment Variables

Required:
- `OPENAI_API_KEY` - Your OpenAI API key

Optional:
- `OPENAI_MODEL` - Default model (default: "gpt-3.5-turbo")
- `OPENAI_MAX_TOKENS` - Default max tokens (default: 1000)
- `OPENAI_TEMPERATURE` - Default temperature (default: 0.7)

## Development

### Adding New Features

1. Update `api/playground.py` with new endpoints
2. Add corresponding tests in `tests/test_playground.py`
3. Update `static/js/playground.js` with helper functions
4. Document in this guide with curl examples

### Best Practices

- Use session IDs for conversation context
- Validate all user inputs
- Handle errors gracefully with user-friendly messages
- Implement rate limiting for production
- Use environment variables for configuration
- Write tests for new endpoints

## Troubleshooting

### Common Issues

**Issue:** "OPENAI_API_KEY NOT CONFIGURED"
- **Solution:** Set the `OPENAI_API_KEY` environment variable

**Issue:** Session not found
- **Solution:** Sessions are in-memory. They reset when server restarts. Use persistent storage for production.

**Issue:** CORS errors
- **Solution:** Configure CORS middleware in `api/index.py` for cross-origin requests

## Production Considerations

- Replace in-memory session storage with Redis or database
- Add authentication and authorization
- Implement rate limiting
- Enable HTTPS
- Add monitoring and logging
- Set up proper error tracking
- Use connection pooling for OpenAI API

## API Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Support

For issues or questions:
- Check API docs at `/docs`
- Review test examples in `tests/test_playground.py`
- See integration examples in `static/js/playground.js`
