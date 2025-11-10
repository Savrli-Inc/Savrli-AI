# Savrli AI Demo Page

A minimal demo page and test harness for manual testing of Savrli AI endpoints.

## Overview

The demo page provides a simple, lightweight interface for testing the AI chat functionality without the full complexity of the main playground. It's designed for quick manual testing and verification of API endpoints.

**Reference:** Issue #36

## Files

- **`pages/demo.html`** - Minimal HTML demo page with sample prompts
- **`static/js/demo.js`** - JavaScript for API integration and UI interactions
- **`tests/test_demo_endpoints.py`** - Basic test suite for demo endpoints

## Features

### Current Features

✅ **Chat Interface**
- Simple text input for prompts
- Sample prompt buttons for quick testing
- Real-time message display
- Session management (demo-session)

✅ **Sample Prompts**
- Quantum computing explanation
- Python code example
- REST API explanation
- Productivity tips

✅ **Response Display**
- Timestamped messages
- Color-coded message types (user, assistant, error)
- Auto-scrolling output
- Clear output functionality

### Planned Features (TODO - Issue #36)

🚧 **File Upload Support**
- Endpoint: `/api/resources/upload` (not yet implemented)
- File selection UI
- Upload progress indicator
- File validation

🚧 **Enhanced UI**
- Better styling and responsive design
- Dark mode support
- Markdown rendering for responses
- Syntax highlighting for code

🚧 **Additional Test Coverage**
- Integration tests for demo.js
- Screenshot testing
- File upload endpoint tests

## Usage

### Accessing the Demo Page

1. Start the Savrli AI server:
   ```bash
   uvicorn api.index:app --reload
   ```

2. Navigate to the demo page:
   ```
   http://localhost:8000/demo
   ```
   
   **Note:** The `/demo` endpoint needs to be added to `api/index.py` (see Setup section below).

### Using the Chat Interface

1. **Enter a prompt** in the text area, or click a sample prompt button
2. **Click "Send"** or press Enter to submit
3. **View the response** in the output section below
4. **Click "Clear Output"** to reset the conversation display

### Sample Prompts

The demo page includes pre-configured sample prompts:
- 🔬 Quantum Computing - "What is quantum computing?"
- 💻 Python Code - "Write a Python function to reverse a string"
- 📚 REST APIs - "Explain REST APIs in simple terms"
- ✨ Productivity - "Give me 3 productivity tips"

## Setup

### Adding the Demo Endpoint

To serve the demo page, add this endpoint to `api/index.py`:

```python
from fastapi.responses import HTMLResponse
from pathlib import Path

@app.get("/demo", response_class=HTMLResponse)
async def demo_page():
    """Serve the demo page for manual testing"""
    demo_path = Path(__file__).parent.parent / "pages" / "demo.html"
    with open(demo_path, "r") as f:
        return HTMLResponse(content=f.read())
```

### Configuring Static File Serving

To serve `static/js/demo.js`, add static file mounting to `api/index.py`:

```python
from fastapi.staticfiles import StaticFiles

# Add after app initialization
app.mount("/static", StaticFiles(directory="static"), name="static")
```

## Testing

### Running Demo Tests

```bash
# Run all demo tests
pytest tests/test_demo_endpoints.py -v

# Run specific test class
pytest tests/test_demo_endpoints.py::TestDemoChatEndpoint -v

# Run with coverage
pytest tests/test_demo_endpoints.py --cov=api --cov=static
```

### Manual Testing Checklist

- [ ] Demo page loads successfully at `/demo`
- [ ] Sample prompt buttons populate the input field
- [ ] Sending a message displays user message in output
- [ ] AI response is received and displayed
- [ ] Timestamps are shown correctly
- [ ] Clear button resets the output display
- [ ] Error messages are displayed appropriately
- [ ] Enter key sends message (Shift+Enter adds new line)

## API Endpoints Used

### `/ai/chat` (POST)

Main chat endpoint for AI conversations.

**Request Body:**
```json
{
  "prompt": "Your question here",
  "model": "gpt-3.5-turbo",
  "temperature": 0.7,
  "max_tokens": 500,
  "session_id": "demo-session"
}
```

**Response:**
```json
{
  "response": "AI response text",
  "session_id": "demo-session",
  "model": "gpt-3.5-turbo"
}
```

### `/api/resources/upload` (POST)

**Status:** Not yet implemented (see issue #36)

Planned endpoint for file uploads to support multimodal testing.

## Screenshots

### Demo Page Interface

![Demo Page](../docs/images/demo-page-placeholder.png)
*TODO: Add screenshot after implementation (issue #36)*

**Placeholder description:**
- Clean, minimal interface
- Sample prompt buttons at top
- Large text area for input
- Send and Clear buttons
- Scrollable output area with timestamped messages

### Chat Interaction

![Chat Interaction](../docs/images/demo-chat-placeholder.png)
*TODO: Add screenshot showing chat interaction (issue #36)*

**Placeholder description:**
- User message in blue
- AI response in purple
- Error messages in red
- Timestamps on each message

## Architecture

### Component Structure

```
demo page (demo.html)
    ├── UI Elements
    │   ├── Sample prompts
    │   ├── Text input
    │   ├── Action buttons
    │   └── Output display
    │
    └── JavaScript (demo.js)
        ├── Event handlers
        ├── API communication
        ├── Response rendering
        └── Error handling
```

### Data Flow

```
User Input → demo.js → /ai/chat endpoint → OpenAI API
                ↓
         Response Display
```

## Known Limitations

1. **No file upload support** - `/api/resources/upload` endpoint not yet implemented
2. **No markdown rendering** - Responses display as plain text
3. **Basic styling** - Minimal CSS, not as polished as main playground
4. **No streaming support** - Responses load all at once
5. **In-memory session only** - No persistence across page reloads

## Future Enhancements (Issue #36)

See issue #36 for detailed roadmap. Key enhancements planned:

1. **File Upload**
   - Implement `/api/resources/upload` endpoint
   - Add file selection UI
   - Support multiple file types
   - Show upload progress

2. **Enhanced UI**
   - Improve styling and layout
   - Add dark mode
   - Implement markdown rendering
   - Add syntax highlighting for code blocks

3. **Better Testing**
   - Add integration tests
   - Implement screenshot tests
   - Add E2E test coverage
   - Mock API responses for offline testing

4. **Additional Features**
   - Conversation export
   - Response copying
   - Model selection dropdown
   - Parameter adjustment controls

## Contributing

When contributing to the demo page:

1. Keep the UI minimal and focused on testing
2. Add TODOs referencing issue #36 for future work
3. Update this documentation with any changes
4. Add tests for new functionality
5. Ensure accessibility (ARIA labels, keyboard navigation)

## Troubleshooting

### Demo page returns 404
- Verify the `/demo` endpoint is added to `api/index.py`
- Check that `pages/demo.html` exists

### demo.js not loading
- Verify static file serving is configured
- Check that `/static` mount is added to `api/index.py`
- Ensure `static/js/demo.js` exists

### API calls failing
- Check that OPENAI_API_KEY is set
- Verify the server is running
- Check browser console for errors
- Ensure request format matches API expectations

### Styles not applying
- Verify demo.html CSS is properly embedded
- Check for browser console errors
- Clear browser cache

## Related Documentation

- [Main README](../README.md)
- [API Documentation](INTEGRATION_API.md)
- [Playground Documentation](../pages/README.md)
- [Issue #36](https://github.com/Savrli-Inc/Savrli-AI/issues/36)

---

**Last Updated:** 2025-11-10  
**Status:** Initial implementation  
**Issue Reference:** #36
