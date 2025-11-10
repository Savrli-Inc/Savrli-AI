# Chat Interface

This directory contains a simple HTML chat interface for the Savrli AI API.

## Files

- `chat.html` - Standalone chat interface

## Usage

### Option 1: Local Testing

1. Open `chat.html` directly in your browser
2. Update the `API_BASE_URL` in the JavaScript section if needed
3. Start chatting!

### Option 2: Serve with Python

```bash
cd public
python3 -m http.server 8000
```

Then visit: http://localhost:8000/chat.html

### Option 3: Deploy with Vercel

The chat interface automatically uses the same origin as your deployed API. Just access:

```
https://your-vercel-url.vercel.app/public/chat.html
```

## Features

✅ **Conversation History** - Messages persist across page reloads using session IDs
✅ **Streaming Responses** - Real-time token-by-token streaming (toggle on/off)
✅ **Session Management** - Unique session ID stored in localStorage
✅ **Clear History** - Button to clear conversation history
✅ **Error Handling** - User-friendly error messages
✅ **Responsive Design** - Works on mobile and desktop
✅ **Typing Indicator** - Shows when AI is processing

## Configuration

The chat interface automatically detects your API URL. If you need to change it:

1. Open `chat.html`
2. Find the line: `const API_BASE_URL = window.location.origin;`
3. Change to your API URL: `const API_BASE_URL = 'https://your-api-url.vercel.app';`

## API Endpoints Used

- `POST /ai/chat` - Send messages
- `GET /ai/history/{session_id}` - Retrieve conversation history
- `DELETE /ai/history/{session_id}` - Clear conversation history
