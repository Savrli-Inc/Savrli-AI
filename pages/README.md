# Pages Directory

This directory contains frontend pages and static HTML content for the Savrli AI application.

## Playground Page

### Overview

`playground.html` is an interactive demo page that provides a user-friendly interface for testing Savrli AI capabilities without writing code.

### Features

- **Model Selection**: Choose between different OpenAI models (GPT-3.5 Turbo, GPT-4, GPT-4 Turbo)
- **Parameter Controls**: Adjust temperature, max tokens, and other AI parameters
- **Conversation History**: Maintain context across multiple messages using session IDs
- **System Instructions**: Customize AI personality and behavior
- **Real-time Feedback**: Loading indicators and user-friendly error messages
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **LocalStorage Persistence**: Conversation history is saved in browser

### How to Use

1. Start the server: `uvicorn api.index:app --reload`
2. Navigate to: `http://localhost:8000/playground`
3. Enter a prompt, adjust settings, and click "Send Message"
4. View AI responses in the output panel

### Customization Guide

#### Updating Colors and Styling

The playground uses CSS custom properties (variables) for easy theming. Update the `:root` section in the `<style>` tag:

```css
:root {
    --primary-color: #6366f1;      /* Main brand color */
    --secondary-color: #8b5cf6;    /* Accent color */
    --background: #0f172a;         /* Page background */
    --surface: #1e293b;            /* Card backgrounds */
    /* ... more variables */
}
```

#### Adding New Parameters

To add a new AI parameter:

1. **Add HTML Input**: Add a new input field in the Configuration section
   ```html
   <div class="settings-group">
       <label for="newParam">New Parameter</label>
       <input type="number" id="newParam" value="1.0">
   </div>
   ```

2. **Capture in JavaScript**: Update the `buildRequestBody()` function
   ```javascript
   function buildRequestBody() {
       const body = {
           // ... existing parameters
           new_param: parseFloat(document.getElementById('newParam').value)
       };
       return body;
   }
   ```

3. **Test**: Verify the parameter is sent to the API

#### Changing the API Endpoint

Update the `API_ENDPOINT` constant in the JavaScript section:

```javascript
const API_ENDPOINT = '/ai/chat'; // Change to your endpoint
```

For external APIs, update to the full URL:

```javascript
const API_ENDPOINT = 'https://api.example.com/chat';
```

#### Adding New Models

Update the `<select id="modelSelect">` options:

```html
<select id="modelSelect">
    <option value="gpt-3.5-turbo">GPT-3.5 Turbo (Fast)</option>
    <option value="gpt-4">GPT-4 (Advanced)</option>
    <option value="your-model">Your Model Name</option>
</select>
```

#### Enabling Streaming Responses

Change the `stream` parameter in `buildRequestBody()`:

```javascript
function buildRequestBody() {
    const body = {
        // ... other parameters
        stream: true  // Enable streaming
    };
    return body;
}
```

Then implement streaming response handling in the `sendMessage()` function using Server-Sent Events (SSE).

### Architecture

The playground is built with:
- **HTML5**: Semantic markup for accessibility
- **CSS3**: Modern styling with flexbox and grid layouts
- **Vanilla JavaScript**: No frameworks required for easy customization

### File Structure

```
playground.html
├── <head>
│   ├── <meta> tags for SEO and mobile responsiveness
│   └── <style> Embedded CSS with custom properties
├── <body>
│   ├── Header with logo and branding
│   ├── Info banner with feature highlights
│   ├── Configuration panel (left side)
│   │   ├── Model selector
│   │   ├── Parameter controls
│   │   ├── Prompt input
│   │   └── Action buttons
│   ├── Response panel (right side)
│   │   └── Message display area
│   └── <script> JavaScript for API interaction
```

### Security Considerations

- **XSS Prevention**: All user input is escaped using `escapeHtml()` function
- **HTTPS**: Use HTTPS in production to protect API keys
- **Input Validation**: Client-side validation prevents empty prompts
- **Error Handling**: API errors don't leak sensitive information

### Browser Compatibility

The playground is compatible with:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

### Testing

The playground endpoint is tested in `tests/test_api.py`:
- HTML response validation
- Required UI elements presence
- API integration code verification
- Documentation completeness

Run tests with:
```bash
python -m pytest tests/test_api.py::TestPlaygroundEndpoint -v
```

### Deployment

The playground is automatically deployed with your FastAPI app. On Vercel:

1. The `/playground` route is accessible at your deployment URL
2. No additional configuration needed
3. Works with serverless functions

### Future Enhancements

Potential improvements:
- Add streaming response support with visual indicators
- Implement syntax highlighting for code responses
- Add export/import conversation functionality
- Include pre-configured example prompts
- Add dark/light theme toggle
- Integrate user authentication
- Add analytics for usage tracking

### Contributing

Contributions are welcome! When modifying the playground:

1. Test all changes locally
2. Ensure responsive design works on mobile
3. Update inline documentation
4. Add tests for new functionality
5. Follow existing code style and patterns

### Support

For issues or questions:
- Open an issue on GitHub
- Check the main README.md for API documentation
- Review inline comments in playground.html
