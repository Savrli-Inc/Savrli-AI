# Contributor Guide

A quick-start guide for new contributors to Savrli AI.

> **Full details**: For comprehensive information, see [CONTRIBUTING.md](../CONTRIBUTING.md)

## 🚀 Quick Start

### 1. How to Pick a Task

**First-time contributors:**
- Look for issues labeled **`good first issue`** or **`First Issue`**
- These are well-documented, beginner-friendly, and often have mentorship available
- Browse issues at: https://github.com/Savrli-Inc/Savrli-AI/issues

**Experienced contributors:**
- Check issues labeled **`help wanted`** for tasks needing attention
- Filter by **priority** labels: `priority:high`, `priority:medium`, `priority:low`
- Look at **area** labels to find tasks in your domain: `area:api`, `area:integration`, `area:testing`, `area:docs`

**Best practices:**
- Start with one issue at a time
- Comment on the issue to let others know you're working on it
- Ask questions if requirements are unclear

### 2. Setup Your Environment

**Automated setup (recommended):**
```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/Savrli-AI.git
cd Savrli-AI

# Run automated setup
python3 setup.py
```

**Manual setup:**
```bash
# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Verify setup works
pytest
```

### 3. How to Run Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run with coverage report
pytest --cov=api --cov=integrations

# Run verbose mode
pytest -v

# Stop at first failure
pytest -x
```

**Before submitting a PR:**
- ✅ All tests must pass
- ✅ Add tests for new features
- ✅ Include tests for bug fixes

### 4. Code Style

**Follow PEP 8 with these conventions:**
- **Line length**: Max 100 characters
- **Type hints**: Use for all function parameters and returns
- **Docstrings**: Use Google-style for public functions
- **Imports**: Organize and sort properly

**Example:**
```python
from typing import Optional, Dict, Any

def process_request(
    prompt: str,
    session_id: Optional[str] = None,
    temperature: float = 0.7
) -> Dict[str, Any]:
    """Process a chat request.

    Args:
        prompt: User's input text
        session_id: Optional session identifier
        temperature: Sampling temperature (0.0-2.0)

    Returns:
        Dictionary with response and metadata

    Raises:
        ValueError: If prompt is empty
    """
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty")
    
    return {"response": "AI reply"}
```

**Code formatting:**
```bash
# Format code (if formatter is configured)
make format

# Run linting (if linter is configured)
make lint
```

### 5. Making Changes

**Branch naming:**
- `feature/` - New features (e.g., `feature/add-temperature-validation`)
- `fix/` - Bug fixes (e.g., `fix/streaming-response-error`)
- `docs/` - Documentation (e.g., `docs/update-api-examples`)
- `test/` - Test additions (e.g., `test/add-streaming-tests`)

**Commit messages (Conventional Commits):**
```bash
feat: add temperature validation to chat endpoint
fix: resolve session history memory leak
docs: update API examples in README
test: add tests for streaming responses
```

**Keep commits:**
- Focused on a single change
- With clear, descriptive messages
- Small and incremental

### 6. Submitting a PR

**Before submitting:**
1. Update your branch: `git pull upstream main`
2. Run tests: `pytest`
3. Check your changes: `git diff`
4. Stage and commit: `git add .` then `git commit`
5. Push: `git push origin your-branch-name`

**PR checklist:**
- [ ] Tests pass
- [ ] Code follows style guidelines
- [ ] Added tests for new functionality
- [ ] Updated documentation if needed
- [ ] PR title follows conventional commits format
- [ ] PR description explains the changes

### 7. Getting Help

**Don't hesitate to ask!**
- 💬 **Questions**: [GitHub Discussions](https://github.com/Savrli-Inc/Savrli-AI/discussions)
- 🐛 **Bug reports**: [GitHub Issues](https://github.com/Savrli-Inc/Savrli-AI/issues)
- 📖 **Documentation**: [docs/](.) directory
- 🤝 **Need mentor**: Comment on the issue

## 📋 Common Tasks

### Running the Server Locally
```bash
# Start the development server
uvicorn api.index:app --reload

# Visit the playground
# Open http://localhost:8000/playground in your browser
```

### Running Integration Tests
```bash
# Test specific integration
pytest tests/test_integrations.py::TestSlackPlugin

# Test all integrations
pytest tests/test_integrations.py
```

### Adding a New Integration
1. Create plugin in `integrations/your_plugin.py`
2. Inherit from `Plugin` base class in `integrations/plugin_base.py`
3. Implement `send_message()` and `process_webhook()` methods
4. Add tests in `tests/test_integrations.py`
5. Document in `docs/PLUGIN_EXAMPLES.md`

### Updating Documentation
- **API changes**: Update `README.md`
- **Integration API**: Update `docs/INTEGRATION_API.md`
- **Examples**: Update `docs/PLUGIN_EXAMPLES.md`
- **Getting started**: Update `docs/ONBOARDING_GUIDE.md`

## 🎯 Tips for Success

1. **Start small** - Pick one issue and do it well
2. **Read existing code** - Understand patterns before writing
3. **Test thoroughly** - Run tests before and after changes
4. **Ask early** - Don't wait until it's "perfect" to get feedback
5. **Follow conventions** - Match existing code style
6. **Be patient** - Code reviews take time
7. **Learn from feedback** - Reviews are learning opportunities

## 📚 Additional Resources

- **Main contribution guide**: [CONTRIBUTING.md](../CONTRIBUTING.md)
- **Onboarding guide**: [docs/ONBOARDING_GUIDE.md](ONBOARDING_GUIDE.md)
- **API documentation**: [README.md](../README.md)
- **Integration examples**: [docs/PLUGIN_EXAMPLES.md](PLUGIN_EXAMPLES.md)
- **Quick start**: [docs/QUICKSTART.md](QUICKSTART.md)

---

**Welcome to Savrli AI!** We're excited to have you contribute. 🚀
