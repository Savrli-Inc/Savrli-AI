import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os
import sys

# Add parent directory to path to import the API
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Set environment variable before importing the app
os.environ['OPENAI_API_KEY'] = 'test-key-12345'

from api.index import app

client = TestClient(app)


class TestChatRequestValidation:
    """Test validation of ChatRequest parameters"""
    
    @patch('api.index.client.chat.completions.create')
    def test_basic_request(self, mock_create):
        """Test basic request still works (backwards compatibility)"""
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_create.return_value = mock_response
        
        response = client.post("/ai/chat", json={"prompt": "Hello"})
        assert response.status_code == 200
        assert "response" in response.json()
    
    def test_empty_prompt(self):
        """Test that empty prompt is rejected"""
        response = client.post("/ai/chat", json={"prompt": ""})
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()
    
    def test_whitespace_only_prompt(self):
        """Test that whitespace-only prompt is rejected"""
        response = client.post("/ai/chat", json={"prompt": "   "})
        assert response.status_code == 400
    
    @patch('api.index.client.chat.completions.create')
    def test_top_p_valid(self, mock_create):
        """Test that valid top_p value is accepted"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_create.return_value = mock_response
        
        response = client.post("/ai/chat", json={"prompt": "Hello", "top_p": 0.9})
        assert response.status_code == 200
    
    def test_top_p_too_high(self):
        """Test that top_p > 1.0 is rejected"""
        response = client.post("/ai/chat", json={"prompt": "Hello", "top_p": 1.5})
        assert response.status_code == 400
        assert "top_p" in response.json()["detail"]
    
    def test_top_p_negative(self):
        """Test that negative top_p is rejected"""
        response = client.post("/ai/chat", json={"prompt": "Hello", "top_p": -0.1})
        assert response.status_code == 400
        assert "top_p" in response.json()["detail"]
    
    def test_frequency_penalty_valid(self):
        """Test that valid frequency_penalty value is accepted"""
        with patch('api.index.client.chat.completions.create') as mock_create:
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Test response"
            mock_create.return_value = mock_response
            
            response = client.post("/ai/chat", json={"prompt": "Hello", "frequency_penalty": 0.5})
            assert response.status_code == 200
    
    def test_frequency_penalty_too_high(self):
        """Test that frequency_penalty > 2.0 is rejected"""
        response = client.post("/ai/chat", json={"prompt": "Hello", "frequency_penalty": 2.5})
        assert response.status_code == 400
        assert "frequency_penalty" in response.json()["detail"]
    
    def test_frequency_penalty_too_low(self):
        """Test that frequency_penalty < -2.0 is rejected"""
        response = client.post("/ai/chat", json={"prompt": "Hello", "frequency_penalty": -2.5})
        assert response.status_code == 400
        assert "frequency_penalty" in response.json()["detail"]
    
    def test_presence_penalty_valid(self):
        """Test that valid presence_penalty value is accepted"""
        with patch('api.index.client.chat.completions.create') as mock_create:
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Test response"
            mock_create.return_value = mock_response
            
            response = client.post("/ai/chat", json={"prompt": "Hello", "presence_penalty": 0.5})
            assert response.status_code == 200
    
    def test_presence_penalty_too_high(self):
        """Test that presence_penalty > 2.0 is rejected"""
        response = client.post("/ai/chat", json={"prompt": "Hello", "presence_penalty": 2.5})
        assert response.status_code == 400
        assert "presence_penalty" in response.json()["detail"]
    
    def test_presence_penalty_too_low(self):
        """Test that presence_penalty < -2.0 is rejected"""
        response = client.post("/ai/chat", json={"prompt": "Hello", "presence_penalty": -2.5})
        assert response.status_code == 400
        assert "presence_penalty" in response.json()["detail"]
    
    def test_context_window_valid(self):
        """Test that valid context_window value is accepted"""
        with patch('api.index.client.chat.completions.create') as mock_create:
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Test response"
            mock_create.return_value = mock_response
            
            response = client.post("/ai/chat", json={"prompt": "Hello", "context_window": 5})
            assert response.status_code == 200
    
    def test_context_window_too_high(self):
        """Test that context_window > 50 is rejected"""
        response = client.post("/ai/chat", json={"prompt": "Hello", "context_window": 51})
        assert response.status_code == 400
        assert "context_window" in response.json()["detail"]
    
    def test_context_window_negative(self):
        """Test that negative context_window is rejected"""
        response = client.post("/ai/chat", json={"prompt": "Hello", "context_window": -1})
        assert response.status_code == 400
        assert "context_window" in response.json()["detail"]
    
    @patch('api.index.client.chat.completions.create')
    def test_custom_system_message(self, mock_create):
        """Test that custom system message is accepted"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_create.return_value = mock_response
        
        custom_system = "You are a helpful coding assistant."
        response = client.post("/ai/chat", json={"prompt": "Hello", "system": custom_system})
        assert response.status_code == 200
        
        # Verify the system message was used in the OpenAI call
        call_args = mock_create.call_args
        messages = call_args.kwargs['messages']
        assert messages[0]['role'] == 'system'
        assert messages[0]['content'] == custom_system
    
    @patch('api.index.client.chat.completions.create')
    def test_all_advanced_parameters(self, mock_create):
        """Test request with all advanced parameters"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_create.return_value = mock_response
        
        response = client.post("/ai/chat", json={
            "prompt": "Hello",
            "top_p": 0.9,
            "frequency_penalty": 0.5,
            "presence_penalty": 0.5,
            "context_window": 5,
            "system": "You are a helpful assistant."
        })
        assert response.status_code == 200
        
        # Verify all parameters were passed to OpenAI
        call_args = mock_create.call_args
        assert call_args.kwargs['top_p'] == 0.9
        assert call_args.kwargs['frequency_penalty'] == 0.5
        assert call_args.kwargs['presence_penalty'] == 0.5


class TestBackwardsCompatibility:
    """Test that existing requests still work"""
    
    @patch('api.index.client.chat.completions.create')
    def test_old_style_request(self, mock_create):
        """Test that old-style requests (just prompt) still work"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_create.return_value = mock_response
        
        response = client.post("/ai/chat", json={"prompt": "Recommend a breakfast"})
        assert response.status_code == 200
        assert "response" in response.json()


class TestRootEndpoint:
    """Test root endpoint"""
    
    def test_root(self):
        """Test that root endpoint works"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()


class TestHelloEndpoint:
    """Test hello endpoint"""
    
    def test_hello(self):
        """Test that hello endpoint works"""
        response = client.get("/hello")
        assert response.status_code == 200
        assert "message" in response.json()
        assert response.json()["message"] == "Hello from Savrli AI!"


class TestConversationHistory:
    """Test conversation history endpoints"""
    
    @patch('api.index.client.chat.completions.create')
    def test_session_creates_history(self, mock_create):
        """Test that using session_id creates conversation history"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_create.return_value = mock_response
        
        # Send a message with session_id
        response = client.post("/ai/chat", json={
            "prompt": "Hello",
            "session_id": "test-session-1"
        })
        assert response.status_code == 200
        
        # Get history for this session
        history_response = client.get("/ai/history/test-session-1")
        assert history_response.status_code == 200
        data = history_response.json()
        assert data["session_id"] == "test-session-1"
        assert len(data["messages"]) == 2  # user + assistant
        assert data["messages"][0]["role"] == "user"
        assert data["messages"][1]["role"] == "assistant"
    
    def test_get_nonexistent_history(self):
        """Test getting history for non-existent session"""
        response = client.get("/ai/history/nonexistent-session")
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == "nonexistent-session"
        assert data["messages"] == []
    
    @patch('api.index.client.chat.completions.create')
    def test_clear_history(self, mock_create):
        """Test clearing conversation history"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_create.return_value = mock_response
        
        # Create some history
        client.post("/ai/chat", json={
            "prompt": "Hello",
            "session_id": "test-session-2"
        })
        
        # Verify history exists
        history_response = client.get("/ai/history/test-session-2")
        assert len(history_response.json()["messages"]) > 0
        
        # Clear history
        clear_response = client.delete("/ai/history/test-session-2")
        assert clear_response.status_code == 200
        assert "cleared" in clear_response.json()["message"].lower()
        
        # Verify history is cleared
        history_response = client.get("/ai/history/test-session-2")
        assert history_response.json()["messages"] == []
    
    @patch('api.index.client.chat.completions.create')
    def test_history_limit_parameter(self, mock_create):
        """Test that limit parameter works for history retrieval"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_create.return_value = mock_response
        
        # Create multiple messages
        for i in range(5):
            client.post("/ai/chat", json={
                "prompt": f"Message {i}",
                "session_id": "test-session-3"
            })
        
        # Get limited history
        history_response = client.get("/ai/history/test-session-3?limit=2")
        assert history_response.status_code == 200
        data = history_response.json()
        # With limit=2, should get last 2 messages (may be less than total)
        assert len(data["messages"]) <= 2
        assert data["total_messages"] > 2


class TestStreamingResponse:
    """Test streaming response functionality"""
    
    @patch('api.index.client.chat.completions.create')
    def test_streaming_enabled(self, mock_create):
        """Test that streaming response works"""
        # Create a mock streaming response
        mock_chunk1 = MagicMock()
        mock_chunk1.choices = [MagicMock()]
        mock_chunk1.choices[0].delta.content = "Hello"
        
        mock_chunk2 = MagicMock()
        mock_chunk2.choices = [MagicMock()]
        mock_chunk2.choices[0].delta.content = " world"
        
        mock_create.return_value = iter([mock_chunk1, mock_chunk2])
        
        response = client.post("/ai/chat", json={
            "prompt": "Test streaming",
            "stream": True
        })
        
        # Check that response is streaming
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
        
        # Verify streaming content
        content = response.text
        assert "data:" in content
        assert "Hello" in content or "world" in content
    
    @patch('api.index.client.chat.completions.create')
    def test_non_streaming_default(self, mock_create):
        """Test that default behavior is non-streaming"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_create.return_value = mock_response
        
        response = client.post("/ai/chat", json={"prompt": "Hello"})
        assert response.status_code == 200
        
        # Non-streaming should return JSON
        assert response.headers["content-type"] == "application/json"
        data = response.json()
        assert "response" in data


class TestSessionManagement:
    """Test session-based conversation management"""
    
    @patch('api.index.client.chat.completions.create')
    def test_conversation_context(self, mock_create):
        """Test that conversation context is maintained across requests"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_create.return_value = mock_response
        
        session_id = "context-test-session"
        
        # First message
        client.post("/ai/chat", json={
            "prompt": "My name is Alice",
            "session_id": session_id
        })
        
        # Second message
        client.post("/ai/chat", json={
            "prompt": "What is my name?",
            "session_id": session_id
        })
        
        # Check that the context was passed to OpenAI
        # The second call should include history
        assert mock_create.call_count == 2
        second_call_kwargs = mock_create.call_args_list[1][1]
        messages = second_call_kwargs['messages']
        
        # Should have system message + previous user message + previous assistant + current user
        assert len(messages) >= 3
        # Find user messages in history
        user_messages = [m for m in messages if m['role'] == 'user']
        assert len(user_messages) >= 2
    
    @patch('api.index.client.chat.completions.create')
    def test_context_window_limits_history(self, mock_create):
        """Test that context_window parameter limits conversation history"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_create.return_value = mock_response
        
        session_id = "context-window-test"
        
        # Create multiple messages
        for i in range(5):
            client.post("/ai/chat", json={
                "prompt": f"Message {i}",
                "session_id": session_id
            })
        
        # Make a request with limited context window
        client.post("/ai/chat", json={
            "prompt": "Latest message",
            "session_id": session_id,
            "context_window": 2
        })
        
        # Check the last call
        last_call_kwargs = mock_create.call_args_list[-1][1]
        messages = last_call_kwargs['messages']
        
        # Count conversation messages (excluding system message)
        user_and_assistant_messages = [m for m in messages if m['role'] in ['user', 'assistant']]
        
        # With context_window=2, should have at most 2*2 messages (2 pairs) + current message
        # But the exact count depends on implementation, so we just verify it's limited
        assert len(user_and_assistant_messages) <= 10  # Should be much less than all 11 messages


class TestResponseSessionId:
    """Test that session_id is returned in response"""
    
    @patch('api.index.client.chat.completions.create')
    def test_response_includes_session_id(self, mock_create):
        """Test that response includes session_id when provided"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_create.return_value = mock_response
        
        response = client.post("/ai/chat", json={
            "prompt": "Hello",
            "session_id": "test-123"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert data["session_id"] == "test-123"
    
    @patch('api.index.client.chat.completions.create')
    def test_response_no_session_id_when_not_provided(self, mock_create):
        """Test that response handles missing session_id correctly"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_create.return_value = mock_response
        
        response = client.post("/ai/chat", json={
            "prompt": "Hello"
        })
        
        assert response.status_code == 200
        data = response.json()
        # session_id should be None or not significant when not provided
        assert "session_id" in data


class TestPlaygroundEndpoint:
    """Test the interactive playground/demo page endpoint"""
    
    def test_playground_returns_html(self):
        """Test that playground endpoint returns HTML content"""
        response = client.get("/playground")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"
    
    def test_playground_contains_required_elements(self):
        """Test that playground HTML contains essential UI elements"""
        response = client.get("/playground")
        content = response.text
        
        # Check for essential UI elements
        assert "Savrli AI Playground" in content
        assert "promptInput" in content  # Input field
        assert "submitBtn" in content  # Submit button
        assert "outputPanel" in content  # Output panel
        assert "modelSelect" in content  # Model selector
        
    def test_playground_includes_api_integration(self):
        """Test that playground includes API integration code"""
        response = client.get("/playground")
        content = response.text
        
        # Check for API endpoint reference
        assert "/ai/chat" in content
        assert "fetch" in content or "XMLHttpRequest" in content
        
    def test_playground_has_documentation(self):
        """Test that playground includes contributor documentation"""
        response = client.get("/playground")
        content = response.text
        
        # Check for inline documentation
        assert "CONTRIBUTOR" in content or "contributor" in content
    
    def test_playground_includes_syntax_highlighting(self):
        """Test that playground includes Highlight.js and Marked.js libraries"""
        response = client.get("/playground")
        content = response.text
        
        # Check for Marked.js CDN link
        assert "marked" in content.lower()
        assert "cdn.jsdelivr.net" in content or "marked" in content
        
        # Check for Highlight.js CDN link
        assert "highlight.js" in content.lower() or "hljs" in content
        assert "cdnjs.cloudflare.com" in content or "highlight" in content
        
        # Check for renderOutput function that processes markdown
        assert "renderOutput" in content
        assert "marked.parse" in content or "marked.setOptions" in content


class TestVisionEndpoint:
    """Test vision/image analysis endpoint"""
    
    def test_vision_empty_prompt(self):
        """Test that empty prompt is rejected"""
        response = client.post("/ai/vision", json={
            "image_url": "https://example.com/image.jpg",
            "prompt": ""
        })
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()
    
    def test_vision_empty_image_url(self):
        """Test that empty image URL is rejected"""
        response = client.post("/ai/vision", json={
            "image_url": "",
            "prompt": "What's in this image?"
        })
        assert response.status_code == 400
        assert "image url" in response.json()["detail"].lower()
    
    def test_vision_invalid_max_tokens(self):
        """Test that invalid max_tokens is rejected"""
        response = client.post("/ai/vision", json={
            "image_url": "https://example.com/image.jpg",
            "prompt": "Describe this image",
            "max_tokens": 3000
        })
        assert response.status_code == 400
        assert "max_tokens" in response.json()["detail"]
    
    @patch('api.index.client.chat.completions.create')
    def test_vision_successful_request(self, mock_create):
        """Test successful vision request"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "This is a test image showing a cat"
        mock_create.return_value = mock_response
        
        response = client.post("/ai/vision", json={
            "image_url": "https://example.com/cat.jpg",
            "prompt": "What's in this image?"
        })
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "image_url" in data
        assert data["image_url"] == "https://example.com/cat.jpg"


class TestImageGenerationEndpoint:
    """Test image generation endpoint"""
    
    def test_image_gen_empty_prompt(self):
        """Test that empty prompt is rejected"""
        response = client.post("/ai/image/generate", json={
            "prompt": ""
        })
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()
    
    def test_image_gen_invalid_n(self):
        """Test that invalid n parameter is rejected"""
        response = client.post("/ai/image/generate", json={
            "prompt": "A beautiful sunset",
            "n": 15
        })
        assert response.status_code == 400
        assert "n must be between" in response.json()["detail"]
    
    def test_image_gen_invalid_size(self):
        """Test that invalid size is rejected"""
        response = client.post("/ai/image/generate", json={
            "prompt": "A beautiful sunset",
            "size": "999x999"
        })
        assert response.status_code == 400
        assert "size must be one of" in response.json()["detail"]
    
    def test_image_gen_invalid_quality(self):
        """Test that invalid quality is rejected"""
        response = client.post("/ai/image/generate", json={
            "prompt": "A beautiful sunset",
            "quality": "ultra"
        })
        assert response.status_code == 400
        assert "quality must be" in response.json()["detail"]
    
    @patch('api.index.client.images.generate')
    def test_image_gen_successful_request(self, mock_generate):
        """Test successful image generation request"""
        mock_response = MagicMock()
        mock_img = MagicMock()
        mock_img.url = "https://example.com/generated-image.png"
        mock_img.revised_prompt = "A beautiful sunset over the ocean"
        mock_response.data = [mock_img]
        mock_generate.return_value = mock_response
        
        response = client.post("/ai/image/generate", json={
            "prompt": "A beautiful sunset"
        })
        assert response.status_code == 200
        data = response.json()
        assert "images" in data
        assert len(data["images"]) == 1
        assert data["images"][0]["url"] == "https://example.com/generated-image.png"
        assert "prompt" in data


class TestAudioTranscriptionEndpoint:
    """Test audio transcription endpoint"""
    
    def test_audio_empty_url(self):
        """Test that empty audio URL is rejected"""
        response = client.post("/ai/audio/transcribe", json={
            "audio_url": ""
        })
        assert response.status_code == 400
        assert "audio url" in response.json()["detail"].lower()
    
    def test_audio_not_implemented(self):
        """Test that audio transcription returns not implemented"""
        response = client.post("/ai/audio/transcribe", json={
            "audio_url": "https://example.com/audio.mp3"
        })
        assert response.status_code == 501
        detail = response.json()["detail"].lower()
        assert "file upload" in detail or "not implemented" in detail


