# Savrli AI Demo Page

A minimal demo page and test harness for manual testing of Savrli AI endpoints.

## Overview
The demo page provides a simple, lightweight interface for testing the AI chat functionality without the full complexity of the main playground. It's designed for quick manual testing and verification of API endpoints.

**Reference:** Issue #36

## Files
- **`pages/demo.html`** – Minimal HTML demo page with sample prompts
- **`static/js/demo.js`** – JavaScript for API integration and UI interactions
- **`tests/test_demo_endpoints.py`** – Basic test suite for demo endpoints

## Features
### Current Features
- **Chat Interface**
  - Simple text input for prompts
  - Sample prompt buttons for quick testing
  - Real-time message display
  - Session management (`demo-session`)
- **Sample Prompts**
  - Quantum computing explanation
  - Python code example
  - REST API explanation
  - Productivity tips
- **Response Display**
  - Timestamped messages
  - Color-coded message types (user, assistant, error)
  - Auto-scrolling output
  - Clear output functionality

### Planned Features (TODO – Issue #36)
- **File Upload Support**
  - Endpoint: `/api/resources/upload`
  - File selection UI
  - Upload progress indicator
  - File validation
- **Enhanced UI**
  - Better styling and responsive design
  - Dark mode support
  - Markdown rendering for responses
  - Syntax highlighting for code
- **Additional Test Coverage**
  - Integration tests for `demo.js`
  - Screenshot testing
  - File upload endpoint tests

## Usage
### Accessing the Demo Page
1. Start the Savrli AI server:
   ```bash
   uvicorn api.index:app --reload
