---
# **Savrli AI Multi-Modal Endpoint**
---

A powerful FastAPI microservice that provides comprehensive AI capabilities using OpenAI's latest models.
It supports text conversations, image analysis, audio transcription, image generation, and model fine-tuning.
Designed for use with the **Savrli app**, deployed on **Vercel**.

> 🌐 **Base URL:** Your endpoint

---

## 🚀 Quick Start Onboarding Checklist

New to Savrli AI? Follow this checklist to get up and running:

- [ ] **Step 1:** Clone the repository
  ```bash
  git clone https://github.com/Savrli-Inc/Savrli-AI.git
  cd Savrli-AI
  ```

- [ ] **Step 2:** Install dependencies
  ```bash
  pip install -r requirements.txt
  ```

- [ ] **Step 3:** Set up environment variables
  - Create a `.env` file in the project root
  - Add your OpenAI API key:
    ```
    OPENAI_API_KEY=your-api-key-here
    ```
  - Optional environment variables:
    ```
    OPENAI_MODEL=gpt-3.5-turbo
    OPENAI_MAX_TOKENS=1000
    OPENAI_TEMPERATURE=0.7
    DEFAULT_CONTEXT_WINDOW=10
    MAX_HISTORY_PER_SESSION=20
    ```

- [ ] **Step 4:** Run the API locally
  ```bash
  uvicorn api.index:app --reload
  ```
  The API will be available at `http://localhost:8000`

- [ ] **Step 5:** Try the interactive playground (recommended for new users)
  - Open `http://localhost:8000/playground` in your browser
  - Use the visual interface to test AI features without writing code

- [ ] **Step 6:** Test with a basic request
  ```bash
  curl -X POST http://localhost:8000/ai/chat \
    -H "Content-Type: application/json" \
    -d '{"prompt": "Hello, how are you?"}'
  ```

- [ ] **Step 7:** Deploy to Vercel (see [Deployment section](#-deployment-vercel))

- [ ] **Step 8:** Test your deployed endpoint with the sample requests below

---

## 📁 Project Structure

```
├── api
│   └── index.py           # Main FastAPI application with multi-modal support
├── ai_capabilities.py     # Multi-modal AI capability classes
├── pages
│   └── playground.html    # Interactive demo/playground page
├── tests
│   ├── test_api.py        # Core API test suite
│   └── test_multimodal.py # Multi-modal features test suite
├── tools
│   └── summarizer.py      # AI text summarization utilities
├── integrations
│   └── discord_plugin.py  # Discord integration plugin
├── postman
│   └── Savrli-AI-Chat.postman_collection.json
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel deployment configuration
└── README.md             # This file
```

**Description:**

* `api/index.py` — Main FastAPI app with text, image, audio, and fine-tuning endpoints
* `ai_capabilities.py` — Multi-modal AI capability classes and model configurations
* `pages/playground.html` — Interactive playground for testing AI features in a browser
* `tests/test_api.py` — Test suite for core API validation and functionality
* `tests/test_multimodal.py` — Test suite for multi-modal features
* `tools/summarizer.py` — AI-powered text summarization utilities
* `integrations/discord_plugin.py` — Discord bot integration
* `requirements.txt` — Python dependencies
* `vercel.json` — Vercel deployment configuration

---

## ⚙️ Overview

This API provides comprehensive AI capabilities using OpenAI's latest models, supporting:
- **Text Processing**: Conversational AI with GPT-3.5 Turbo, GPT-4, and GPT-4 Turbo
- **Image Analysis**: Visual understanding with GPT-4 Vision
- **Image Generation**: Create images from text with DALL-E 2 and DALL-E 3
- **Audio Processing**: Transcribe audio with Whisper
- **Model Fine-tuning**: Configure custom model training

The API supports both stateless (one-off) and stateful (session-based) conversations with conversation history tracking.

### **Core Features**

✅ **Multi-Modal Processing** - Text, image, and audio input/output support  
✅ **Custom AI Behavior** - Define assistant personality via system instructions  
✅ **Conversation History** - Multi-turn conversations with session management  
✅ **Streaming Responses** - Real-time token streaming for better UX  
✅ **Advanced Controls** - Fine-tune AI output with OpenAI parameters  
✅ **Image Analysis** - Analyze and describe images with GPT-4 Vision  
✅ **Image Generation** - Create images from text prompts with DALL-E  
✅ **Audio Transcription** - Convert speech to text with Whisper  
✅ **Model Fine-tuning** - Configure custom training datasets  
✅ **Input Validation** - Comprehensive error handling and validation  
✅ **History Management** - View and clear conversation history via API  
✅ **Interactive Playground** - Visual interface for testing AI features  

---

## 🎮 Interactive Playground

The Savrli AI Playground provides a user-friendly web interface for testing and experimenting with AI capabilities without writing code.

### **Access the Playground**

Once your server is running, visit:
```
http://localhost:8000/playground
```

Or on your deployed Vercel instance:
```
https://your-project.vercel.app/playground
```

### **Playground Features**

🎯 **Model Selection** - Choose between GPT-3.5 Turbo, GPT-4, and GPT-4 Turbo  
⚙️ **Parameter Controls** - Adjust temperature, max tokens, and other OpenAI parameters  
💬 **Conversation History** - Maintain context across multiple messages  
🎨 **System Instructions** - Customize AI personality and behavior  
📊 **Real-time Feedback** - See loading states and error messages  
📱 **Responsive Design** - Works on desktop, tablet, and mobile devices  

### **Perfect For**

- **Onboarding**: New users can understand AI capabilities through hands-on interaction
- **Testing**: Quickly validate API functionality and response quality
- **Demos**: Showcase AI features to stakeholders without technical setup
- **Experimentation**: Try different parameters and prompts to optimize results

### **Contributing to the Playground**

The playground is built with vanilla HTML/CSS/JavaScript for easy customization:

- **Styling**: Update CSS variables in `pages/playground.html` to match your brand
- **API Endpoint**: Modify `API_ENDPOINT` constant for different backends
- **New Parameters**: Add inputs in HTML and capture in `buildRequestBody()` function
- **UI Enhancements**: The code includes inline comments to guide modifications

---

## 🔌 API Endpoints

### **Text Processing**

#### 1. **Chat Endpoint**

`POST /ai/chat`

Main endpoint for generating AI text responses with full feature support.

#### 2. **Get Conversation History**

`GET /ai/history/{session_id}?limit=50`

Retrieve conversation history for a specific session.

#### 3. **Clear Conversation History**

`DELETE /ai/history/{session_id}`

Clear all conversation history for a specific session.

### **Image Processing**

#### 4. **Image Analysis (Vision)**

`POST /ai/vision`

Analyze images using GPT-4 Vision. Accepts image URL or base64-encoded image data.

#### 5. **Image Generation**

`POST /ai/image/generate`

Generate images from text prompts using DALL-E 2 or DALL-E 3.

### **Audio Processing**

#### 6. **Audio Transcription**

`POST /ai/audio/transcribe`

Transcribe audio files to text using Whisper API. Supports multiple audio formats.

### **Model Management**

#### 7. **List Available Models**

`GET /ai/models`

List all supported AI models and their capabilities (text, image, audio).

#### 8. **Get Model Information**

`GET /ai/models/{model_name}`

Get detailed information about a specific model.

#### 9. **Configure Fine-tuning**

`POST /ai/fine-tune/configure`

Configure fine-tuning parameters for custom model training.

### **Utility Endpoints**

#### 10. **Interactive Playground**

`GET /playground`

Serves the interactive demo page for testing AI features in a browser.

#### 11. **Health Check**

`GET /`

Returns API status confirmation.

---

## 📝 Request Parameters

### **Required Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | string | User's text input (required, non-empty) |

### **Optional Parameters**

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `session_id` | string | - | None | Session identifier for conversation history |
| `system` | string | - | Default assistant | Custom system instruction defining AI behavior |
| `stream` | boolean | - | false | Enable Server-Sent Events streaming |
| `model` | string | - | gpt-3.5-turbo | OpenAI model to use |
| `max_tokens` | integer | 1-2000 | 1000 | Maximum tokens in response |
| `temperature` | float | 0.0-2.0 | 0.7 | Sampling temperature (higher = more random) |
| `top_p` | float | 0.0-1.0 | - | Nucleus sampling parameter |
| `frequency_penalty` | float | -2.0 to 2.0 | - | Penalize token frequency (reduce repetition) |
| `presence_penalty` | float | -2.0 to 2.0 | - | Penalize token presence (increase diversity) |
| `context_window` | integer | 0-50 | 10 | Number of previous conversation turns to include |

---

## 📡 Response Codes & Error Handling

| Status Code | Meaning | When It Occurs | Example Response |
|-------------|---------|----------------|------------------|
| **200** | ✅ Success | Valid request processed successfully | `{"response": "AI reply", "session_id": "user-123"}` |
| **400** | ⚠️ Bad Request | Invalid input parameters | `{"detail": "Prompt cannot be empty"}` |
| **400** | ⚠️ Bad Request | Parameter out of range | `{"detail": "temperature must be between 0.0 and 2.0"}` |
| **400** | ⚠️ Bad Request | Invalid max_tokens | `{"detail": "max_tokens must be between 1 and 2000"}` |
| **400** | ⚠️ Bad Request | Invalid top_p | `{"detail": "top_p must be between 0.0 and 1.0"}` |
| **400** | ⚠️ Bad Request | Invalid frequency_penalty | `{"detail": "frequency_penalty must be between -2.0 and 2.0"}` |
| **400** | ⚠️ Bad Request | Invalid presence_penalty | `{"detail": "presence_penalty must be between -2.0 and 2.0"}` |
| **400** | ⚠️ Bad Request | Invalid context_window | `{"detail": "context_window must be between 0 and 50"}` |
| **502** | ❌ Bad Gateway | OpenAI returned unexpected response format | `{"detail": "AI returned an empty response"}` |
| **503** | ❌ Service Unavailable | OpenAI API failure, rate limit, or network issue | `{"detail": "AI temporarily unavailable"}` |

### **Common Error Scenarios**

1. **Empty Prompt**: Submit a non-empty prompt string
2. **Invalid Temperature**: Use a value between 0.0 and 2.0
3. **OpenAI API Issues**: Check your API key and quota
4. **Rate Limiting**: Implement retry logic with exponential backoff

---

## 🧪 Example Requests

### **1. Basic Chat Request**

Simple one-off conversation without history.

```bash
curl -X POST https://your-api-url/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Recommend a quick breakfast recipe"
  }'
```

**Response:**
```json
{
  "response": "How about scrambled eggs with avocado toast and a side of orange juice?",
  "session_id": null
}
```

---

### **2. Chat with Custom System Instructions**

Define the AI's personality and expertise.

```bash
curl -X POST https://your-api-url/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Python function to calculate fibonacci",
    "system": "You are an expert Python developer who writes clean, well-documented code."
  }'
```

---

### **3. Conversational Chat with History**

Multi-turn conversation with context awareness.

```bash
# First message
curl -X POST https://your-api-url/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is the capital of France?",
    "session_id": "user-123"
  }'

# Follow-up message (AI remembers previous context)
curl -X POST https://your-api-url/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is its population?",
    "session_id": "user-123"
  }'
```

---

### **4. Advanced Request with All Parameters**

Fine-tuned AI behavior with custom parameters.

```bash
curl -X POST https://your-api-url/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain quantum computing simply",
    "system": "You are a patient teacher explaining complex topics to beginners.",
    "session_id": "user-456",
    "model": "gpt-3.5-turbo",
    "temperature": 0.8,
    "top_p": 0.9,
    "frequency_penalty": 0.3,
    "presence_penalty": 0.3,
    "max_tokens": 500,
    "context_window": 5
  }'
```

---

### **5. Streaming Response**

Get real-time streaming responses using Server-Sent Events.

```bash
curl -X POST https://your-api-url/ai/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Tell me a short story",
    "stream": true
  }'
```

**Response (SSE format):**
```
data: {"content": "Once"}

data: {"content": " upon"}

data: {"content": " a"}

data: {"content": " time"}

data: {"done": true}
```

**JavaScript Example for Streaming:**
```javascript
const eventSource = new EventSource('/ai/chat');
eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.done) {
    eventSource.close();
  } else if (data.content) {
    console.log(data.content); // Append to UI
  } else if (data.error) {
    console.error(data.error);
    eventSource.close();
  }
};
```

---

### **6. Get Conversation History**

Retrieve conversation history for a session.

```bash
curl -X GET https://your-api-url/ai/history/user-123?limit=10
```

**Response:**
```json
{
  "session_id": "user-123",
  "messages": [
    {
      "role": "user",
      "content": "What is the capital of France?",
      "timestamp": "2025-11-08T12:00:00.000Z"
    },
    {
      "role": "assistant",
      "content": "The capital of France is Paris.",
      "timestamp": "2025-11-08T12:00:01.000Z"
    }
  ],
  "total_messages": 2
}
```

---

### **7. Clear Conversation History**

Delete all conversation history for a session.

```bash
curl -X DELETE https://your-api-url/ai/history/user-123
```

**Response:**
```json
{
  "message": "History cleared for session user-123"
}
```

---

### **8. Image Analysis with GPT-4 Vision**

Analyze images using GPT-4 Vision with image URL.

```bash
curl -X POST https://your-api-url/ai/vision \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What objects are in this image?",
    "image_url": "https://example.com/image.jpg",
    "detail": "high"
  }'
```

**Response:**
```json
{
  "response": "This image contains a laptop, a coffee cup, and some notebooks on a wooden desk.",
  "model": "gpt-4-vision-preview",
  "input_type": "image"
}
```

**With Base64 Image:**
```bash
curl -X POST https://your-api-url/ai/vision \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Describe this image in detail",
    "image_base64": "iVBORw0KGgoAAAANSUhEUgAAAA...",
    "max_tokens": 500
  }'
```

---

### **9. Generate Images with DALL-E**

Create images from text prompts using DALL-E 3.

```bash
curl -X POST https://your-api-url/ai/image/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A serene landscape with mountains and a lake at sunset",
    "model": "dall-e-3",
    "size": "1024x1024",
    "quality": "hd",
    "style": "vivid"
  }'
```

**Response:**
```json
{
  "images": [
    {
      "url": "https://oaidalleapiprodscus.blob.core.windows.net/...",
      "revised_prompt": "A serene landscape featuring majestic mountains..."
    }
  ],
  "model": "dall-e-3",
  "count": 1
}
```

**Using DALL-E 2:**
```bash
curl -X POST https://your-api-url/ai/image/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cute robot playing guitar",
    "model": "dall-e-2",
    "size": "512x512",
    "n": 2
  }'
```

---

### **10. Transcribe Audio with Whisper**

Convert audio files to text using Whisper API.

```bash
curl -X POST https://your-api-url/ai/audio/transcribe \
  -F "file=@/path/to/audio.mp3" \
  -F "model=whisper-1" \
  -F "language=en" \
  -F "response_format=json"
```

**Response:**
```json
{
  "transcription": "Hello, this is a test audio transcription.",
  "model": "whisper-1",
  "input_type": "audio"
}
```

**With Additional Context:**
```bash
curl -X POST https://your-api-url/ai/audio/transcribe \
  -F "file=@/path/to/meeting.mp3" \
  -F "prompt=This is a business meeting discussion" \
  -F "response_format=verbose_json"
```

---

### **11. List Available Models**

Get information about all supported AI models.

```bash
curl -X GET https://your-api-url/ai/models
```

**Response:**
```json
{
  "models": [
    {
      "model_name": "gpt-4",
      "capabilities": ["text"]
    },
    {
      "model_name": "gpt-4-vision-preview",
      "capabilities": ["text", "image"]
    },
    {
      "model_name": "whisper-1",
      "capabilities": ["audio"]
    },
    {
      "model_name": "dall-e-3",
      "capabilities": ["text", "image"]
    }
  ],
  "total_count": 10,
  "capabilities": {
    "text": ["gpt-4", "gpt-4-turbo-preview", "gpt-3.5-turbo"],
    "image_analysis": ["gpt-4-vision-preview"],
    "image_generation": ["dall-e-3", "dall-e-2"],
    "audio": ["whisper-1", "tts-1", "tts-1-hd"]
  }
}
```

---

### **12. Get Model Information**

Get detailed information about a specific model.

```bash
curl -X GET https://your-api-url/ai/models/gpt-4-vision-preview
```

**Response:**
```json
{
  "model_name": "gpt-4-vision-preview",
  "capabilities": ["text", "image"],
  "status": "available"
}
```

---

### **13. Configure Fine-tuning**

Configure parameters for fine-tuning a custom model.

```bash
curl -X POST https://your-api-url/ai/fine-tune/configure \
  -H "Content-Type: application/json" \
  -d '{
    "training_file": "file-abc123xyz",
    "model": "gpt-3.5-turbo",
    "validation_file": "file-def456uvw",
    "n_epochs": 5,
    "batch_size": "4",
    "learning_rate_multiplier": "0.1",
    "suffix": "custom-support-bot"
  }'
```

**Response:**
```json
{
  "configuration": {
    "training_file": "file-abc123xyz",
    "model": "gpt-3.5-turbo",
    "validation_file": "file-def456uvw",
    "hyperparameters": {
      "n_epochs": 5,
      "batch_size": "4",
      "learning_rate_multiplier": "0.1"
    },
    "suffix": "custom-support-bot"
  },
  "status": "configured",
  "message": "Fine-tuning configuration ready - use API endpoints to start fine-tuning",
  "note": "Use OpenAI's fine-tuning API to start the actual fine-tuning job with this configuration"
}
```

---

## 🚀 Deployment (Vercel)

### **Prerequisites**

1. GitHub account with your repository
2. Vercel account (free tier works)
3. OpenAI API key

### **Deployment Steps**

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Link to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import your GitHub repository

3. **Configure Environment Variables**
   
   In Vercel dashboard, add these environment variables:
   
   **Required:**
   ```
   OPENAI_API_KEY = your-openai-api-key
   ```
   
   **Optional (with defaults):**
   ```
   OPENAI_MODEL = gpt-3.5-turbo
   OPENAI_MAX_TOKENS = 1000
   OPENAI_TEMPERATURE = 0.7
   DEFAULT_CONTEXT_WINDOW = 10
   MAX_HISTORY_PER_SESSION = 20
   ```

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Your API will be live at `https://your-project.vercel.app`

5. **Test Deployment**
   ```bash
   curl -X POST https://your-project.vercel.app/ai/chat \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello!"}'
   ```

### **vercel.json Configuration**

The project includes a `vercel.json` file that configures the deployment:

```json
{
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

---

## 🧰 Environment Variables

Configure these in your `.env` file for local development or in Vercel dashboard for production:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | - | Your OpenAI API key |
| `OPENAI_MODEL` | No | gpt-3.5-turbo | Default model for requests |
| `OPENAI_MAX_TOKENS` | No | 1000 | Default max tokens per response |
| `OPENAI_TEMPERATURE` | No | 0.7 | Default temperature (randomness) |
| `DEFAULT_CONTEXT_WINDOW` | No | 10 | Default conversation history size |
| `MAX_HISTORY_PER_SESSION` | No | 20 | Maximum messages stored per session |

---

## 🧪 Testing

### **Run Tests Locally**

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_api.py -v
python -m pytest tests/test_multimodal.py -v

# Run specific test class
python -m pytest tests/test_api.py::TestChatRequestValidation -v
python -m pytest tests/test_multimodal.py::TestVisionEndpoint -v

# Run with coverage
python -m pytest tests/ --cov=api --cov-report=html
```

### **Test Coverage**

The comprehensive test suite includes **54 tests** covering:

**Core API Tests (test_api.py):**
- ✅ Input validation for all parameters
- ✅ Error handling and edge cases
- ✅ Custom system instructions
- ✅ Conversation history management
- ✅ Advanced OpenAI parameters
- ✅ Streaming responses
- ✅ Session management
- ✅ Backwards compatibility

**Multi-Modal Tests (test_multimodal.py):**
- ✅ Image analysis with GPT-4 Vision
- ✅ Image generation with DALL-E 2 and DALL-E 3
- ✅ Audio transcription with Whisper
- ✅ Model listing and information retrieval
- ✅ Fine-tuning configuration
- ✅ Multi-modal integration testing

---

## 🔧 Troubleshooting

### **General Issues**

#### **Issue: "OPENAI_API_KEY is not set"**
**Solution:** Set the environment variable in `.env` file or Vercel dashboard.

#### **Issue: "AI temporarily unavailable" (503 error)**
**Solution:** Check your OpenAI API key, quota, and network connectivity.

#### **Issue: "temperature must be between 0.0 and 2.0" (400 error)**
**Solution:** Ensure all parameters are within valid ranges (see [Request Parameters](#-request-parameters)).

#### **Issue: Empty or missing responses**
**Solution:** Check OpenAI API status and your API quota. Enable logging to see detailed errors.

#### **Issue: Streaming not working**
**Solution:** Ensure your client supports Server-Sent Events (SSE). Check the streaming example above.

### **Multi-Modal Issues**

#### **Issue: "Form data requires python-multipart to be installed"**
**Solution:** Install the required package: `pip install python-multipart`

#### **Issue: Vision endpoint returns error "image_url or image_base64 must be provided"**
**Solution:** Provide either `image_url` (URL to image) or `image_base64` (base64-encoded image data) in your request.

#### **Issue: Image generation fails with "Invalid size" error**
**Solution:** Ensure you're using valid sizes for the selected model:
- DALL-E 3: `1024x1024`, `1792x1024`, or `1024x1792`
- DALL-E 2: `256x256`, `512x512`, or `1024x1024`

#### **Issue: Audio transcription fails**
**Solution:** 
- Verify the audio file format is supported (mp3, mp4, mpeg, mpga, m4a, wav, webm)
- Check file size is under OpenAI's limits
- Ensure the file is properly uploaded as multipart form data

#### **Issue: Model not found (404 error)**
**Solution:** Use the `/ai/models` endpoint to get a list of available models and verify the model name.

---

## 🤖 Supported AI Models

### **Text Generation Models**
| Model | Capabilities | Best For |
|-------|-------------|----------|
| `gpt-4` | Advanced text generation | Complex reasoning, detailed analysis |
| `gpt-4-turbo-preview` | Fast text generation | High-performance applications |
| `gpt-3.5-turbo` | Efficient text generation | General-purpose chatbots, cost-effective |

### **Vision Models**
| Model | Capabilities | Best For |
|-------|-------------|----------|
| `gpt-4-vision-preview` | Image understanding + text | Image analysis, visual Q&A, OCR |

### **Image Generation Models**
| Model | Capabilities | Supported Sizes |
|-------|-------------|-----------------|
| `dall-e-3` | High-quality image generation | 1024x1024, 1792x1024, 1024x1792 |
| `dall-e-2` | Fast image generation | 256x256, 512x512, 1024x1024 |

### **Audio Models**
| Model | Capabilities | Best For |
|-------|-------------|----------|
| `whisper-1` | Speech-to-text transcription | Audio transcription, meeting notes |
| `tts-1` | Text-to-speech synthesis | Voice generation (standard quality) |
| `tts-1-hd` | High-definition text-to-speech | Voice generation (high quality) |

### **Fine-tuning Support**
Fine-tuning is available for:
- ✅ `gpt-3.5-turbo` - Best for custom chatbots and specialized tasks
- ✅ `gpt-4` - Available for enterprise customers

Use the `/ai/fine-tune/configure` endpoint to set up fine-tuning parameters.

---

## 📚 Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [GPT-4 Vision Guide](https://platform.openai.com/docs/guides/vision)
- [DALL-E Image Generation](https://platform.openai.com/docs/guides/images)
- [Whisper Audio Transcription](https://platform.openai.com/docs/guides/speech-to-text)
- [Fine-tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vercel Python Deployment](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Server-Sent Events (SSE)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes and add tests
4. Run tests to ensure everything passes
5. Commit your changes (`git commit -m 'Add new feature'`)
6. Push to your branch (`git push origin feature/your-feature`)
7. Open a Pull Request

---

## 📄 License

This project is part of the Savrli platform. All rights reserved.

---

## 🔗 Links

- **Repository:** [Savrli-Inc/Savrli-AI](https://github.com/Savrli-Inc/Savrli-AI)
- **Issues:** [Report an issue](https://github.com/Savrli-Inc/Savrli-AI/issues)
- **Discussions:** [Join the discussion](https://github.com/Savrli-Inc/Savrli-AI/discussions)

---

**Made with ❤️ by the Savrli Team**
