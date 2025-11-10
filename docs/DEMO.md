# Savrli AI Demo Page

## Overview
The **Savrli AI Demo Page** is an interactive test harness for manually testing the **chat and file upload endpoints**. It offers a clean, developer-friendly UI to verify API behavior without writing code.

Perfect for:
- Quick API validation
- Demoing features to stakeholders
- Debugging integrations

---

## Access
| Environment | URL |
|-----------|-----|
| **Local** | `http://localhost:8000/demo` |
| **Production** | `https://your-domain.vercel.app/demo` |

---

## Features

### 1. **Chat API Demo** (`POST /ai/chat`)
- **Quick Test Buttons** – One-click prompts:
  - Geography Question
  - Science Explanation
  - Creative Writing
  - Health Question
  - Recipe Request
  - Fun Fact
- **Custom Prompt Form** – Full control:
  - Free-text input
  - Optional `session_id` for conversation continuity

**Response Display**:
- Real-time loading spinner
- Formatted AI response
- Raw JSON toggle
- Session ID metadata

---

### 2. **Resource Upload Demo** (`POST /api/resources/upload`)
- File picker (any type: images, audio, PDF, JSON, text)
- Live preview of:
  - Filename
  - Content type
  - File size (human-readable)
- Upload progress indicator
- Success/error feedback
- Raw JSON response

---

## Manual Testing Guide

### Test Chat Functionality
1. Open `/demo`
2. **Quick Test**:
   - Click **"Geography Question"**
   - Wait for loading spinner
   - Verify response contains **"Paris, France"**
3. **Custom Test**:
   - Enter: `Explain quantum entanglement in simple terms`
   - Set `session_id: user-123`
   - Click **Send**
   - Follow-up: `What did I just ask?` → should recall

### Test File Upload
1. Scroll to **"Resource Upload Demo"**
2. Choose a file:
   - `test.jpg` (image)
   - `recipe.json`
   - `voice.mp3`
3. Click **Upload File**
4. Verify response includes:
   ```json
   {
     "success": true,
     "file_info": {
       "filename": "test.jpg",
       "content_type": "image/jpeg",
       "size": 245760,
       "size_formatted": "240.00 KB"
     }
   }