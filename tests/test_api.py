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
