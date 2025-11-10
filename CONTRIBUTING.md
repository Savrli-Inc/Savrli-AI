# Contributing to Savrli AI

Thank you for your interest in contributing to Savrli AI! We welcome contributions from the community and are grateful for your support.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Branch Naming Conventions](#branch-naming-conventions)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Requirements](#testing-requirements)
- [Integration Development](#integration-development)
- [Documentation](#documentation)

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Savrli-AI.git
   cd Savrli-AI
   ```

3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/Savrli-Inc/Savrli-AI.git
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

6. **Run tests** to ensure everything is working:
   ```bash
   pytest
   ```

## Development Workflow

### 1. Create a Feature Branch

Always create a new branch for your work:

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Write clean, readable code
- Follow the code style guidelines
- Add tests for new functionality
- Update documentation as needed

### 3. Keep Your Branch Updated

Regularly sync with upstream:

```bash
git fetch upstream
git rebase upstream/main
```

### 4. Run Tests and Linting

Before committing, ensure your code passes all checks:

```bash
# Run tests
pytest

# Run linting
make lint

# Format code
make format
```

### 5. Commit Your Changes

Follow the commit message guidelines (see below).

### 6. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 7. Open a Pull Request

Submit a PR from your fork to the main repository.

## Branch Naming Conventions

Use descriptive branch names that follow this pattern:

- `feature/` - New features or enhancements
  - Example: `feature/add-temperature-validation`
  - Example: `feature/slack-integration`

- `fix/` - Bug fixes
  - Example: `fix/streaming-response-error`
  - Example: `fix/session-history-leak`

- `docs/` - Documentation updates
  - Example: `docs/update-api-examples`
  - Example: `docs/add-deployment-guide`

- `refactor/` - Code refactoring without feature changes
  - Example: `refactor/simplify-history-manager`
  - Example: `refactor/extract-validation-logic`

- `test/` - Adding or updating tests
  - Example: `test/add-streaming-tests`
  - Example: `test/improve-coverage`

- `chore/` - Maintenance tasks
  - Example: `chore/update-dependencies`
  - Example: `chore/setup-ci`

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

### Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Code style changes (formatting, missing semi-colons, etc.)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to build process or auxiliary tools
- `perf`: Performance improvements
- `ci`: CI/CD configuration changes

### Examples

```bash
# Good commit messages
feat: add temperature validation to chat endpoint
fix: resolve session history memory leak
docs: update API examples in README
test: add tests for streaming responses
refactor: extract validation logic to separate module
chore: update dependencies to latest versions

# With scope
feat(integrations): add Discord webhook support
fix(api): handle empty OpenAI responses correctly
test(api): add validation tests for all parameters

# With body
feat: add streaming response support

Implement Server-Sent Events (SSE) for real-time token streaming.
This allows clients to receive AI responses progressively.

Closes #123
```

### Commit Message Best Practices

- Use the imperative mood ("add" not "added" or "adds")
- Keep the subject line under 50 characters
- Capitalize the subject line
- Do not end the subject line with a period
- Separate subject from body with a blank line
- Wrap the body at 72 characters
- Use the body to explain what and why, not how
- Reference issues and pull requests in the footer

## Pull Request Process

### Before Submitting

1. **Update your branch** with the latest changes from `main`
2. **Run all tests** and ensure they pass
3. **Run linting** and fix any issues
4. **Update documentation** if needed
5. **Add tests** for new functionality
6. **Test manually** if applicable

### PR Title

Use the same format as commit messages:

```
feat: add temperature validation to chat endpoint
fix: resolve session history memory leak
docs: update deployment instructions
```

### PR Description Template

Include the following in your PR description:

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)

## Testing
- [ ] All existing tests pass
- [ ] Added new tests for new functionality
- [ ] Manually tested the changes

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

## Related Issues
Closes #issue_number (if applicable)
```

### Review Process

- At least one maintainer must approve the PR
- All CI checks must pass
- Address all review comments
- Keep the PR focused on a single concern
- Be responsive to feedback

### Merging

- PRs are typically merged using "Squash and Merge" to maintain a clean history
- The PR title becomes the commit message
- Ensure the commit message is clear and descriptive

## Code Style Guidelines

### Python Style

We follow [PEP 8](https://peps.python.org/pep-0008/) with some additional conventions:

- **Line length**: Maximum 100 characters
- **Imports**: Organized and sorted
- **Type hints**: Use type hints for function parameters and return values
- **Docstrings**: Use Google-style docstrings

### Example

```python
from typing import Optional, Dict, Any

def process_chat_request(
    prompt: str,
    session_id: Optional[str] = None,
    temperature: float = 0.7
) -> Dict[str, Any]:
    """Process a chat request and return the AI response.

    Args:
        prompt: User's input text
        session_id: Optional session identifier for conversation history
        temperature: Sampling temperature between 0.0 and 2.0

    Returns:
        Dictionary containing the AI response and metadata

    Raises:
        ValueError: If prompt is empty or temperature is out of range
    """
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")
    
    # Implementation...
    return {"response": "AI reply", "session_id": session_id}
```

### Code Organization

- Keep functions focused and single-purpose
- Limit function length to ~50 lines
- Use descriptive variable and function names
- Avoid magic numbers; use constants
- Group related functionality into modules

### Error Handling

```python
# Good: Specific error handling with context
try:
    response = client.chat.completions.create(...)
except OpenAIError as e:
    logger.error(f"OpenAI API error: {e}")
    raise HTTPException(
        status_code=503,
        detail="AI service temporarily unavailable"
    )

# Bad: Generic error handling
try:
    response = client.chat.completions.create(...)
except Exception:
    pass
```

## Testing Requirements

### Test Coverage

- All new features must include tests
- Bug fixes should include regression tests
- Aim for >80% code coverage
- Test both success and error cases

### Writing Tests

```python
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

class TestNewFeature:
    """Test suite for new feature"""
    
    @patch('api.index.client.chat.completions.create')
    def test_feature_success(self, mock_create):
        """Test successful execution"""
        # Setup
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Test response"
        mock_create.return_value = mock_response
        
        # Execute
        response = client.post("/ai/chat", json={"prompt": "Test"})
        
        # Assert
        assert response.status_code == 200
        assert "response" in response.json()
    
    def test_feature_validation_error(self):
        """Test validation error handling"""
        response = client.post("/ai/chat", json={"prompt": ""})
        assert response.status_code == 400
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run specific test class
pytest tests/test_api.py::TestChatRequestValidation

# Run with coverage
pytest --cov=api --cov=integrations --cov-report=html

# Run with verbose output
pytest -v

# Run and stop at first failure
pytest -x
```

## Integration Development

### Adding a New Integration

1. Create a new plugin file in `integrations/`:
   ```python
   from integrations.plugin_base import Plugin
   
   class YourPlatformPlugin(Plugin):
       def __init__(self, config: dict):
           super().__init__("your-platform", config)
       
       def send_message(self, channel: str, message: str, **kwargs):
           # Implementation
           pass
       
       def process_webhook(self, payload: dict):
           # Implementation
           pass
   ```

2. Add tests in `tests/test_integrations.py`
3. Document the integration in `docs/PLUGIN_EXAMPLES.md`
4. Update the integration list in `README.md`
5. Add environment variables to `.env.example`

### Integration Best Practices

- Validate configuration on initialization
- Provide clear error messages
- Handle rate limits and retries
- Log important events
- Support webhook verification
- Include comprehensive tests

## Documentation

### Documentation Requirements

- Update `README.md` for user-facing changes
- Update API documentation for endpoint changes
- Add inline comments for complex logic
- Include docstrings for all public functions
- Provide examples for new features

### Documentation Style

- Use clear, concise language
- Include code examples
- Provide both basic and advanced examples
- Keep examples up to date
- Use proper markdown formatting

### Files to Update

- `README.md` - Main project documentation
- `docs/INTEGRATION_API.md` - Integration API documentation
- `docs/PLUGIN_EXAMPLES.md` - Integration examples
- `CHANGELOG.md` - Version history
- Inline code comments - Complex logic

## Questions or Need Help?

- **General questions**: Open a [Discussion](https://github.com/Savrli-Inc/Savrli-AI/discussions)
- **Bug reports**: Open an [Issue](https://github.com/Savrli-Inc/Savrli-AI/issues)
- **Feature requests**: Open an [Issue](https://github.com/Savrli-Inc/Savrli-AI/issues) with the `enhancement` label
- **Security issues**: Email the maintainers directly (do not open a public issue)

## License

By contributing to Savrli AI, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Savrli AI! 🚀
