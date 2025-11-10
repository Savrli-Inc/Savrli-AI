# GitHub Copilot Instructions for Savrli AI

## Repository Overview

Savrli AI is a FastAPI microservice that provides conversational AI capabilities using OpenAI's GPT models. It supports both stateless and stateful conversations with advanced features like streaming responses, conversation history, and customizable AI behavior. The service is designed for integration with the Savrli app and is deployed on Vercel.

## Tech Stack

- **Backend Framework**: FastAPI
- **AI Provider**: OpenAI (GPT-3.5-turbo, GPT-4)
- **Runtime**: Python 3.x with uvicorn
- **Testing**: pytest with httpx for async tests
- **Deployment**: Vercel (serverless)
- **Dependencies**: pydantic for validation, python-dotenv for environment management

## Architecture Patterns

### Plugin Architecture
The codebase uses a plugin-based architecture for third-party integrations:
- Base plugin interface defined in `integrations/plugin_base.py`
- All plugins inherit from the `Plugin` abstract base class
- Plugins must implement `send_message()` and `process_webhook()` methods
- Plugin manager handles registration and lifecycle

### API Structure
- Main application in `api/index.py`
- Request/response models use Pydantic BaseModel
- Conversation history stored in-memory (consider Redis for production)
- Session-based conversation tracking with `session_id`

## Development Guidelines

### Code Style
- Follow PEP 8 Python style guide
- Use type hints for function parameters and return values
- Add docstrings for all public functions and classes
- Keep functions focused and single-purpose
- Use descriptive variable names

### Error Handling
- Always validate environment variables on startup (fail fast)
- Use FastAPI's HTTPException for API errors with appropriate status codes
- Log errors with context using the logging module
- Provide clear error messages to API consumers

### Environment Variables
Required environment variables:
- `OPENAI_API_KEY` (required, fails on startup if missing)

Optional environment variables with defaults:
- `OPENAI_MODEL` (default: "gpt-3.5-turbo")
- `OPENAI_MAX_TOKENS` (default: 1000)
- `OPENAI_TEMPERATURE` (default: 0.7)
- `DEFAULT_CONTEXT_WINDOW` (default: 10)
- `MAX_HISTORY_PER_SESSION` (default: 20)

### Testing Conventions
- Tests located in `tests/` directory
- Use pytest as the testing framework
- Mock external API calls (OpenAI, platform integrations)
- Set `OPENAI_API_KEY` environment variable in test setup
- Use FastAPI's TestClient for endpoint testing
- Test both success and error cases
- Include validation tests for request models

### Adding New Endpoints
1. Define Pydantic models for request/response
2. Implement the endpoint handler in `api/index.py`
3. Add comprehensive error handling
4. Write tests in `tests/test_api.py`
5. Update API documentation in README.md
6. Consider rate limiting and security implications

### Adding New Integrations
1. Create a new plugin file in `integrations/` (e.g., `platform_plugin.py`)
2. Inherit from the `Plugin` base class in `plugin_base.py`
3. Implement required abstract methods: `send_message()` and `process_webhook()`
4. Register the plugin in `api/index.py` plugin manager
5. Add endpoint handlers for the integration
6. Write tests in `tests/test_integrations.py`
7. Document the integration in `docs/` directory

## Security Best Practices
- Never commit API keys or secrets to the repository
- Use environment variables for all sensitive configuration
- Validate and sanitize all user inputs
- Implement rate limiting for production deployments
- Use HTTPS for all production endpoints
- Follow OpenAI's usage policies and content guidelines

## API Response Patterns
- Use consistent response structure across endpoints
- Include appropriate HTTP status codes
- Provide meaningful error messages
- Support streaming responses where appropriate
- Return metadata (timestamps, session info) when relevant

## Documentation
- Keep README.md up to date with API changes
- Document all endpoints with request/response examples
- Include integration examples in `docs/PLUGIN_EXAMPLES.md`
- Update `docs/INTEGRATION_API.md` for plugin API changes
- Use curl examples for clarity

## Common Patterns

### Request Validation
```python
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    prompt: str
    session_id: Optional[str] = None
    model: Optional[str] = Field(default=None, pattern="^gpt-")
```

### OpenAI Client Usage
```python
response = client.chat.completions.create(
    model=model,
    messages=messages,
    max_tokens=max_tokens,
    temperature=temperature
)
```

### Plugin Pattern
```python
class CustomPlugin(Plugin):
    def send_message(self, channel: str, message: str, **kwargs) -> Dict[str, Any]:
        # Implementation
        pass
    
    def process_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # Implementation
        pass
```

## Running Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY=your-api-key

# Run the server
uvicorn api.index:app --reload
```

## Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=api --cov=integrations

# Run specific test file
pytest tests/test_api.py
```

## Deployment Notes
- Vercel deployment configured in `vercel.json`
- Environment variables must be set in Vercel dashboard
- API runs as serverless functions
- Consider cold start implications for response times

## When Making Changes
1. Understand the existing code structure before making changes
2. Run tests before and after changes
3. Update documentation if adding/changing public APIs
4. Consider backward compatibility
5. Follow the principle of minimal changes
6. Add or update tests for new functionality
7. Check that environment variable changes are documented
