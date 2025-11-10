# Savrli AI Demo Page Documentation

## Overview

The Savrli AI Demo Page is an interactive test harness designed for manual testing and demonstration of the playground and multimodal endpoints. It provides a user-friendly interface to test the core AI capabilities without writing code.

## Features

### 1. Chat Endpoint Demo (`POST /ai/chat`)
- Pre-configured sample prompts for quick testing
- Interactive buttons for common use cases
- Real-time response display
- Loading indicators during API calls

### 2. Resource Upload Demo (`POST /resources/upload`)
- File selection interface
- Support for multiple file types (images, audio, text, PDF, JSON)
- File metadata display
- Upload status feedback

## Accessing the Demo

### Local Development
```bash
# Start the server
uvicorn api.index:app --reload

# Open in browser
http://localhost:8000/demo
```

### Production (Vercel)
```
https://your-deployment.vercel.app/demo
```

## Manual Testing Steps

### Testing Chat Functionality

1. **Navigate to Demo Page**
   - Open `/demo` in your web browser
   - Verify the page loads successfully

2. **Test Sample Prompts**
   - Click the "Geography Question" button
   - Observe the loading indicator
   - Verify response appears in the chat response box
   - Expected: Response contains information about Paris, France

3. **Test Different Prompt Types**
   - Try each pre-configured button:
     - 🗺️ Geography Question
     - 🔬 Science Explanation
     - ✍️ Creative Writing
     - 💪 Health Question
     - 🍳 Recipe Request
     - 🌌 Fun Fact
   - Verify each returns an appropriate response
   - Check for errors in browser console

4. **Verify Response Display**
   - Check that responses are properly formatted
   - Verify loading states change correctly
   - Ensure error messages display when API is unavailable

### Testing File Upload Functionality

1. **Select a File**
   - Click the file input in the "Resource Upload Demo" section
   - Choose a test file (e.g., image, text file, or JSON)
   - Verify file information displays (name and size)

2. **Upload the File**
   - Click the "Upload File" button
   - Observe the upload loading indicator
   - Verify upload response appears with metadata

3. **Test Different File Types**
   - Upload an image file (PNG, JPG)
   - Upload a text file (TXT)
   - Upload a JSON file
   - Upload an audio file (MP3, WAV)
   - Verify each upload completes successfully

4. **Verify Response Metadata**
   - Check that response includes:
     - Success status
     - Filename
     - Content type
     - File size
   - Verify size is formatted correctly (KB/MB)

### Error Handling Tests

1. **Test Without File Selection**
   - Click "Upload File" without selecting a file
   - Expected: Error message "Please select a file to upload"

2. **Test API Unavailability**
   - Stop the API server
   - Try clicking a chat demo button
   - Expected: Error message with connection details

3. **Test Invalid Requests**
   - Check browser console for any JavaScript errors
   - Verify error messages are user-friendly

## Screenshots

### Main Demo Page
![Demo Page Overview](images/demo-overview.png)
*Screenshot placeholder: Overall view of the demo page showing both chat and upload sections*

### Chat Demo in Action
![Chat Demo](images/demo-chat.png)
*Screenshot placeholder: Chat endpoint demo with a sample response displayed*

### Upload Demo with File Selected
![Upload Demo](images/demo-upload.png)
*Screenshot placeholder: Upload section with file selected and response metadata*

### Loading States
![Loading Indicators](images/demo-loading.png)
*Screenshot placeholder: Demo showing loading indicators during API calls*

### Error Handling
![Error Display](images/demo-error.png)
*Screenshot placeholder: Demo showing error message when API is unavailable*

## API Endpoints Used

### Chat Endpoint
```
POST /ai/chat
Content-Type: application/json

{
  "prompt": "Your question here",
  "max_tokens": 500,
  "temperature": 0.7
}
```

**Response:**
```json
{
  "response": "AI generated response text",
  "session_id": null
}
```

### Upload Endpoint
```
POST /resources/upload
Content-Type: multipart/form-data

file: <binary file data>
```

**Response:**
```json
{
  "success": true,
  "filename": "example.txt",
  "content_type": "text/plain",
  "size": 1234,
  "size_formatted": "1.21 KB",
  "message": "File 'example.txt' uploaded successfully"
}
```

## Troubleshooting

### Demo Page Not Loading

**Issue:** Accessing `/demo` returns 404 or shows "Demo page not found"

**Solution:**
1. Verify `pages/demo.html` exists in the repository
2. Check that the server has restarted after adding the demo page
3. Review server logs for any startup errors

### Static Files (demo.js) Not Loading

**Issue:** Browser console shows 404 error for `/static/js/demo.js`

**Solution:**
1. Verify `static/js/demo.js` exists in the repository
2. Check that FastAPI StaticFiles is properly mounted
3. Ensure the static directory path is correct
4. For Vercel deployments, verify static files are included in deployment

### Chat Responses Not Appearing

**Issue:** Clicking chat buttons shows loading but no response appears

**Solution:**
1. Check browser console for JavaScript errors
2. Verify `OPENAI_API_KEY` environment variable is set
3. Check network tab for API response status
4. Review server logs for OpenAI API errors
5. Ensure the OpenAI API key has sufficient credits

### Upload Fails

**Issue:** File upload returns error or doesn't complete

**Solution:**
1. Check file size limits (if configured)
2. Verify file type is supported
3. Check network tab for upload request details
4. Review server logs for upload endpoint errors
5. Ensure file permissions are correct on the server

### CORS Errors

**Issue:** Browser console shows CORS-related errors

**Solution:**
1. Verify FastAPI CORS middleware is configured (if needed)
2. Check that requests are being made to the correct origin
3. For local development, ensure port numbers match

## Future Enhancements

### Planned Features
- [ ] Streaming response support (see TODOs in demo.js)
- [ ] Session management for chat history
- [ ] Custom prompt input field
- [ ] Response export functionality
- [ ] Dark mode toggle
- [ ] Advanced parameter controls (temperature, max_tokens, etc.)
- [ ] File preview before upload
- [ ] Multiple file upload support
- [ ] Upload progress bar

### Streaming Implementation

The demo.js file includes TODOs for implementing streaming response rendering. To enable this:

1. Add stream support to chat request
2. Use ReadableStream or EventSource to consume SSE
3. Progressively update the response container
4. Add animation for streaming text

See comments in `/static/js/demo.js` for detailed implementation guidance.

## Development Notes

### File Structure
```
Savrli-AI/
├── pages/
│   └── demo.html          # Demo page HTML
├── static/
│   └── js/
│       └── demo.js        # Demo page JavaScript
├── tests/
│   └── test_demo_endpoints.py  # Demo endpoint tests
├── docs/
│   └── DEMO.md           # This documentation
└── api/
    └── index.py          # API with /demo and /resources/upload endpoints
```

### Adding New Sample Prompts

To add new sample prompts to the demo page:

1. Edit `pages/demo.html`
2. Add a new button in the `.demo-grid` section:
```html
<button class="demo-button chat-demo-btn" data-prompt="Your prompt here">
    <span class="demo-button-label">🎯 Label</span>
    <span class="demo-button-prompt">"Your prompt here"</span>
</button>
```

### Styling Customization

The demo page uses inline CSS for simplicity. To customize:

1. Edit the `<style>` section in `pages/demo.html`
2. Modify CSS custom properties in the `:root` selector
3. Adjust colors, spacing, or layout as needed

## Testing

### Running Automated Tests

```bash
# Run all demo tests
pytest tests/test_demo_endpoints.py -v

# Run specific test class
pytest tests/test_demo_endpoints.py::TestDemoPageEndpoint -v

# Run with coverage
pytest tests/test_demo_endpoints.py --cov=api --cov-report=html
```

### Test Coverage

The test suite includes:
- ✅ Demo page endpoint (returns 200)
- ✅ HTML content validation
- ✅ Chat endpoint integration
- ✅ Upload endpoint functionality
- ✅ File metadata validation
- ✅ Multiple file type support
- ✅ Error handling
- ✅ Static file serving

## Security Considerations

### Input Validation
- All file uploads are validated on the server
- File size limits should be configured for production
- Content types are checked and logged

### API Key Security
- Never expose OpenAI API keys in client-side code
- Ensure `.env` file is in `.gitignore`
- Use environment variables for all secrets

### Rate Limiting
- Consider implementing rate limiting for production
- Monitor API usage to prevent abuse
- Set appropriate timeouts for requests

## Support

For issues or questions about the demo page:

1. Check this documentation first
2. Review server logs for error messages
3. Check browser console for JavaScript errors
4. Refer to main [README.md](../README.md) for API documentation
5. Open an issue on GitHub with reproduction steps

## Related Documentation

- [API Documentation](../README.md)
- [Playground Guide](../pages/README.md)
- [Integration API](INTEGRATION_API.md)
- [Quickstart Guide](QUICKSTART.md)
