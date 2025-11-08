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

