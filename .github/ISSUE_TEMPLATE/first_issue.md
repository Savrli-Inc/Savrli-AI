---
name: First Issue
about: Template for first-time contributors - claim your first task and get started!
title: '[FIRST ISSUE] '
labels: 'First Issue, good first issue'
assignees: ''
---

## 👋 Welcome, First-Time Contributor!

Thank you for your interest in contributing to Savrli AI! This issue is specifically designed for newcomers to the project.

---

## 📋 Issue Description

<!-- Maintainer: Provide a clear, concise description of the task -->

**What needs to be done:**


**Why it's important:**


**Expected outcome:**


---

## 🎯 Getting Started

If you'd like to work on this issue, follow these steps:

### 1. Claim the Issue

Comment below to let us know you're interested:
```
Hi! I'd like to work on this issue. I've completed the setup following the onboarding guide.
```

**Please wait for a maintainer to assign you before starting work!** This prevents duplicate efforts.

### 2. Set Up Your Development Environment

If you haven't already, complete the setup process:

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/Savrli-Inc/Savrli-AI.git
cd Savrli-AI

# Run the automated setup script
./scripts/setup.sh
```

**The setup script will:**
- ✅ Check your Python version (3.8+ required)
- ✅ Optionally create a virtual environment
- ✅ Install all dependencies
- ✅ Help configure environment variables
- ✅ Run basic health checks
- ✅ Show you next steps

**Need help?** See our comprehensive [Onboarding Guide](../docs/ONBOARDING.md) for:
- Step-by-step setup instructions
- Troubleshooting common issues
- Environment variable configuration
- Testing and verification steps

### 3. Create a Feature Branch

```bash
# Make sure you're on main branch
git checkout main

# Pull latest changes
git pull origin main

# Create a new branch for your work
git checkout -b feature/issue-NUMBER-brief-description
```

**Example branch names:**
- `feature/issue-42-add-temperature-validation`
- `fix/issue-18-session-memory-leak`
- `docs/issue-35-update-readme-examples`

### 4. Make Your Changes

- Follow the coding style in [CONTRIBUTING.md](../CONTRIBUTING.md)
- Add tests for new functionality
- Update documentation as needed
- Test your changes thoroughly

### 5. Test Your Changes

```bash
# Run the test suite
pytest tests/ -v

# Start the server and test manually
uvicorn api.index:app --reload

# Visit http://localhost:8000/playground to test interactively
```

### 6. Commit and Push

```bash
# Stage your changes
git add .

# Commit with a clear message (see CONTRIBUTING.md for format)
git commit -m "feat: brief description of change"

# Push to your fork
git push origin feature/issue-NUMBER-brief-description
```

### 7. Open a Pull Request

- Open a PR from your branch to `main`
- Reference this issue in the PR description: `Closes #ISSUE_NUMBER`
- Fill out the PR template completely
- Wait for review and address feedback

---

## 📚 Helpful Resources

### Documentation
- **[Onboarding Guide](../docs/ONBOARDING.md)** - Complete setup and troubleshooting guide
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Contribution guidelines, code style, testing
- **[README.md](../README.md)** - Full API documentation and examples
- **[Setup Script](../scripts/setup.sh)** - Automated development environment setup

### Getting Help
- **Questions about setup?** Check [docs/ONBOARDING.md](../docs/ONBOARDING.md#troubleshooting)
- **Questions about this issue?** Comment below
- **General questions?** Use [GitHub Discussions](https://github.com/Savrli-Inc/Savrli-AI/discussions)
- **Found a bug?** Open a new [issue](https://github.com/Savrli-Inc/Savrli-AI/issues)

### Key Commands Reference

```bash
# Setup (first time only)
./scripts/setup.sh

# Activate virtual environment (if created)
source venv/bin/activate

# Start development server
uvicorn api.index:app --reload

# Run tests
pytest tests/ -v

# Run specific test
pytest tests/test_api.py -v

# Run tests with coverage
pytest --cov=api --cov=integrations tests/
```

---

## ✅ Acceptance Criteria

<!-- Maintainer: List specific, measurable criteria for completion -->

The PR will be considered complete when:

- [ ] <!-- Criterion 1 -->
- [ ] <!-- Criterion 2 -->
- [ ] All existing tests pass
- [ ] New tests added (if applicable)
- [ ] Documentation updated (if applicable)
- [ ] Code follows project style guidelines

---

## 💡 Implementation Hints

<!-- Maintainer: Optional hints or guidance for the contributor -->

**Files you'll likely need to modify:**


**Key concepts to understand:**


**Helpful tips:**


---

## 🤝 Mentorship Available

As a first-time contributor, you're welcome to:
- ✅ Ask questions in the comments (no question is too basic!)
- ✅ Request code review at any stage (early feedback is encouraged!)
- ✅ Ask for help if you get stuck
- ✅ Take your time to learn and understand the codebase

**We're here to help you succeed!** This is a learning opportunity, and we're happy to guide you through the process.

---

## 📝 Notes for Maintainers

<!-- Internal notes - contributors can ignore this section -->

**Estimated difficulty:** Easy / Medium / Hard  
**Estimated time:** X hours  
**Prerequisites:**  
**Related issues:**  

---

## 🎉 After Your PR is Merged

Congratulations on your first contribution! Here's what to do next:

1. **Celebrate!** You're now a Savrli AI contributor! 🎊
2. **Look for more "First Issue" labeled tasks** - Build your skills
3. **Try a slightly more challenging issue** - Level up
4. **Help other first-timers** - Share your experience
5. **Join our community** - Stay connected with the project

Thank you for contributing to Savrli AI! ❤️
