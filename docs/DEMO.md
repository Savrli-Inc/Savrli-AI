# Savrli AI Demo Page

## Overview

The Savrli AI Demo page provides a simple, interactive test harness for manually testing the playground and multimodal endpoints. It offers a minimal UI for developers and testers to quickly verify API functionality without writing code.

## Access

The demo page is available at:
- **Local Development:** `http://localhost:8000/demo`
- **Production:** `https://your-domain.vercel.app/demo`

## Features

### 1. Chat API Demo (`/ai/chat`)

The chat demo section allows you to test the conversational AI endpoint with:

- **Quick Test Prompts**: Pre-configured buttons for common test scenarios
  - AI Fun Fact
  - Coding Haiku
  - Quantum Computing (with session ID)
  
- **Custom Prompt Form**: Free-form input for testing custom queries
  - Prompt text area
  - Optional session ID for conversation continuity
  
**Screenshot Placeholder:**
```
[Screenshot: Chat API Demo Section]
- Show the quick test buttons
- Show the custom prompt form
- Show a sample response in the output panel
```

### 2. Resource Upload API Demo (`/api/resources/upload`)

The upload demo section provides:

- **File Upload Interface**: Simple file selector for testing uploads
- **File Metadata Display**: Shows information about uploaded files
  - Filename
  - Content type
  - File size

**Screenshot Placeholder:**
```
[Screenshot: Upload API Demo Section]
- Show the file input selector
- Show upload button
- Show sample upload result with file metadata
```

## Usage Guide

### Testing Chat Functionality

1. Navigate to `/demo` in your browser
2. Choose a test method:
   - **Quick Test**: Click one of the pre-configured buttons
   - **Custom Test**: Fill in the custom prompt form
3. View the response in the output panel below
4. Check the raw JSON response in the expandable section

**Example Usage:**

```javascript
// The demo page makes requests like this:
POST /ai/chat
{
  "prompt": "Hello! Tell me a fun fact about artificial intelligence.",
  "session_id": null  // optional
}
```

### Testing File Upload

1. Navigate to the "Resource Upload API Demo" section
2. Click "Choose File" and select a file from your system
3. Click "Upload File" button
4. View the upload result including file metadata

**Example Response:**

```json
{
  "success": true,
  "message": "File uploaded successfully",
  "file_info": {
    "filename": "test.txt",
    "content_type": "text/plain",
    "size": 1234
  }
}
```

## API Endpoints Tested

### Chat Endpoint

- **URL:** `POST /ai/chat`
- **Parameters:**
  - `prompt` (required): The user's message
  - `session_id` (optional): For conversation continuity
  - Additional optional parameters: `max_tokens`, `temperature`, `model`, etc.
- **Response:** JSON with `response` field and optional `session_id`

### Upload Endpoint

- **URL:** `POST /api/resources/upload`
- **Parameters:**
  - `file` (required): File upload via multipart/form-data
- **Response:** JSON with file metadata

## Technical Details

### Files

- **HTML Page:** `/pages/demo.html`
  - Minimal responsive design
  - Mobile-friendly layout
  - Dark theme matching playground
  
- **JavaScript:** `/static/js/demo.js`
  - API integration functions
  - Response rendering
  - Error handling
  - XSS protection via HTML escaping

- **Tests:** `/tests/test_demo_endpoints.py`
  - Endpoint availability tests
  - Static file serving tests
  - Integration tests

### Architecture

```
┌─────────────────┐
│   Demo Page     │
│  (demo.html)    │
└────────┬────────┘
         │
         ├──> /static/js/demo.js (JavaScript)
         │
         ├──> POST /ai/chat (Chat API)
         │
         └──> POST /api/resources/upload (Upload API)
```

## Development

### Running Locally

```bash
# Start the server
uvicorn api.index:app --reload

# Access demo page
open http://localhost:8000/demo
```

### Running Tests

```bash
# Run all demo tests
pytest tests/test_demo_endpoints.py -v

# Run specific test class
pytest tests/test_demo_endpoints.py::TestDemoPageEndpoint -v
```

### Adding New Test Prompts

Edit `/pages/demo.html` and add new buttons in the "Quick Test Prompts" section:

```html
<button class="chat-demo-btn" data-prompt="Your prompt here">
    🎯 Button Label
</button>
```

## UI Components

### Output Panels

Both chat and upload sections have output panels that display:
- **Loading State**: Animated spinner during API calls
- **Success State**: Formatted response with metadata
- **Error State**: Error messages with red border
- **Raw JSON**: Collapsible section with full API response

### Styling

The demo page uses a minimal dark theme with:
- CSS variables for easy customization
- Responsive design (mobile-first)
- Consistent with playground styling
- Focus on functionality over aesthetics

## Screenshots

**Screenshot Placeholder 1: Full Demo Page**
```
[Screenshot: Full demo page view]
- Header with title and description
- Both demo sections visible
- Clean, minimal dark theme
```

**Screenshot Placeholder 2: Chat Response**
```
[Screenshot: Chat API response display]
- Show a successful chat response
- Metadata showing session ID
- Raw JSON section expanded
```

**Screenshot Placeholder 3: Upload Success**
```
[Screenshot: File upload success]
- File metadata displayed
- Size formatted in human-readable format
- Raw JSON response visible
```

**Screenshot Placeholder 4: Error State**
```
[Screenshot: Error handling]
- Show error message in output panel
- Red border on error panel
- Clear error description
```

**Screenshot Placeholder 5: Mobile View**
```
[Screenshot: Demo page on mobile]
- Responsive layout
- Buttons stacked vertically
- Touch-friendly interface
```

## Troubleshooting

### Common Issues

**Issue:** Demo page shows "Demo page not found"
- **Solution:** Ensure `pages/demo.html` exists and server has read permissions

**Issue:** JavaScript not loading
- **Solution:** Check that static files are mounted correctly in `api/index.py`

**Issue:** Upload fails with 422 error
- **Solution:** Ensure file is selected before clicking upload button

**Issue:** Chat returns 503 error
- **Solution:** Verify `OPENAI_API_KEY` is set in environment variables

### Debug Tips

1. Open browser developer console (F12) to see JavaScript errors
2. Check Network tab to see actual API requests/responses
3. Use raw JSON section to inspect full API responses
4. Check server logs for backend errors

## Future Enhancements

Potential improvements for the demo page:

- [ ] Add vision API demo with image upload
- [ ] Add audio transcription demo
- [ ] Add streaming response visualization
- [ ] Add request/response timing metrics
- [ ] Add ability to save and share test configurations
- [ ] Add syntax highlighting for code in responses
- [ ] Add export functionality for test results

## Contributing

When adding new features to the demo page:

1. Keep the UI minimal and functional
2. Update this documentation
3. Add corresponding tests in `test_demo_endpoints.py`
4. Ensure mobile responsiveness
5. Follow existing code style and patterns

## Related Documentation

- [API Documentation](/docs)
- [Playground Guide](/playground)
- [Integration API](INTEGRATION_API.md)
- [Quick Start Guide](QUICKSTART.md)

---

**Note:** This is a development and testing tool. For production integrations, use the API directly or integrate via the official SDKs.
