# Visual Assets for Documentation

This directory contains screenshots, GIFs, and other visual assets used in the documentation.

## Recommended Assets to Add

To enhance the onboarding experience, consider adding these visual guides:

### Setup & Installation
- `setup-python-success.png` - Screenshot of successful Python setup script execution
- `setup-bash-success.png` - Screenshot of successful Bash setup script execution
- `environment-setup.gif` - Animated GIF showing .env file configuration
- `dependency-install.png` - Screenshot of successful dependency installation

### Playground Interface
- `playground-overview.png` - Full screenshot of the playground interface
- `playground-first-message.gif` - Animated GIF of sending first message
- `playground-model-selection.png` - Screenshot showing model selection dropdown
- `playground-parameters.png` - Screenshot of parameter configuration section
- `playground-conversation.png` - Screenshot of a multi-turn conversation

### API Testing
- `curl-first-request.gif` - Animated GIF of making first curl request
- `postman-collection.png` - Screenshot of Postman collection import
- `api-response-success.png` - Screenshot of successful API response
- `api-docs-swagger.png` - Screenshot of auto-generated Swagger docs

### Development Workflow
- `test-run-success.png` - Screenshot of successful pytest execution
- `test-coverage-report.png` - Screenshot of coverage report
- `server-startup.png` - Screenshot of server startup with welcome message
- `hot-reload-demo.gif` - Animated GIF showing hot reload in action

### Troubleshooting
- `error-api-key-missing.png` - Screenshot of API key error with solution
- `error-dependency-missing.png` - Screenshot of dependency error
- `error-port-in-use.png` - Screenshot of port conflict error

### Integration Examples
- `slack-integration.png` - Screenshot of Slack integration in action
- `discord-integration.png` - Screenshot of Discord bot interaction
- `notion-integration.png` - Screenshot of Notion page creation

## File Naming Conventions

- Use lowercase with hyphens: `my-screenshot.png`
- Use descriptive names: `playground-first-message.gif` not `img1.gif`
- Include context: `error-api-key-missing.png` not `error.png`

## Image Formats

- **Screenshots**: PNG format (better for UI with text)
- **Photos**: JPG format (better for photographs)
- **Animations**: GIF format (for short demos, < 5MB)
- **Diagrams**: SVG format (scalable, crisp at any size)

## Recommended Tools

### For Screenshots
- **macOS**: Cmd+Shift+4 (built-in)
- **Windows**: Snipping Tool or Snip & Sketch
- **Linux**: GNOME Screenshot, Flameshot, or Shutter

### For GIFs
- **All Platforms**: [LICEcap](https://www.cockos.com/licecap/) (free, simple)
- **macOS**: [Kap](https://getkap.co/) (free, feature-rich)
- **Windows**: [ScreenToGif](https://www.screentogif.com/) (free)
- **Online**: [ezgif.com](https://ezgif.com/) (for editing/optimization)

### For Optimization
- **PNGs**: [TinyPNG](https://tinypng.com/)
- **JPGs**: [JPEG Optimizer](http://jpeg-optimizer.com/)
- **GIFs**: [ezgif.com](https://ezgif.com/optimize)

## Contributing Visual Assets

When adding new images:

1. **Optimize file sizes** - Keep images under 1MB when possible
2. **Use clear, high-quality screenshots** - Text should be readable
3. **Annotate when helpful** - Use arrows, highlights, or callouts
4. **Keep it current** - Update screenshots when UI changes
5. **Follow naming conventions** - Make files easy to find
6. **Add alt text in docs** - Describe images for accessibility

## Usage in Documentation

Reference images in Markdown like this:

```markdown
![Playground Interface](docs/images/playground-overview.png)

*Figure 1: The Savrli AI Playground interface*
```

For animated GIFs:
```markdown
![First API Request](docs/images/curl-first-request.gif)

*Animation: Making your first API request with curl*
```

## Current Assets

<!-- Update this list when adding new images -->

Currently, this directory contains placeholder documentation. Visual assets will be added as they are created.

---

**Note**: This is a placeholder directory structure. Contributors are encouraged to add screenshots and GIFs to enhance the onboarding experience!
