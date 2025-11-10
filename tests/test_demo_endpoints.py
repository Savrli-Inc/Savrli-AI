"""
Test suite for demo page endpoints

Basic tests to verify demo endpoints return 200 status codes.
These are simple smoke tests to ensure the demo page is accessible.

TODO (issue #36): Expand test coverage for:
- File upload endpoint when /api/resources/upload is implemented
- Integration testing with demo.js
- Screenshot testing for UI verification
"""

import pytest
from fastapi.testclient import TestClient
import os
import sys

# Add parent directory to path to import the API
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Set environment variable before importing the app
os.environ['OPENAI_API_KEY'] = 'test-key-12345'

from api.index import app

client = TestClient(app)


class TestDemoPageEndpoint:
    """Test the demo page HTML endpoint"""
    
    def test_demo_page_exists(self):
        """Verify /demo returns 200 and HTML content"""
        response = client.get("/demo")
        assert response.status_code == 200
    
    def test_demo_page_returns_html(self):
        """Verify demo page serves HTML content type"""
        response = client.get("/demo")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_demo_page_contains_required_elements(self):
        """Verify demo page contains essential UI elements"""
        response = client.get("/demo")
        assert response.status_code == 200
        content = response.text
        
        # Check for essential elements
        assert "Savrli AI Demo" in content
        assert "promptInput" in content
        assert "sendButton" in content
        assert "output" in content
        assert "/static/js/demo.js" in content
        assert "issue #36" in content.lower() or "issue #36" in content


class TestDemoStaticAssets:
    """Test static assets for demo page"""
    
    def test_demo_js_accessible(self):
        """Verify demo.js is accessible via static file serving"""
        response = client.get("/static/js/demo.js")
        assert response.status_code == 200
    
    def test_demo_js_valid_javascript(self):
        """Verify demo.js contains expected JavaScript code"""
        response = client.get("/static/js/demo.js")
        assert response.status_code == 200
        content = response.text
        
        # Check for key functions
        assert "initDemo" in content
        assert "sendChatMessage" in content
        assert "CHAT_ENDPOINT" in content
        assert "issue #36" in content.lower() or "issue #36" in content


class TestDemoChatEndpoint:
    """Test that demo page can interact with /ai/chat endpoint"""
    
    def test_chat_endpoint_accessible_for_demo(self):
        """Verify /ai/chat endpoint is accessible (required for demo)"""
        # This endpoint already exists, verify it returns 200 with valid request
        from unittest.mock import patch, MagicMock
        
        with patch('api.index.client.chat.completions.create') as mock_create:
            # Mock OpenAI response
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Test response for demo"
            mock_create.return_value = mock_response
            
            response = client.post("/ai/chat", json={
                "prompt": "Test prompt from demo page",
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "max_tokens": 500,
                "session_id": "demo-session"
            })
            
            assert response.status_code == 200
            assert "response" in response.json()
    
    def test_chat_endpoint_handles_demo_session(self):
        """Verify demo session is handled correctly"""
        from unittest.mock import patch, MagicMock
        
        with patch('api.index.client.chat.completions.create') as mock_create:
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Demo session response"
            mock_create.return_value = mock_response
            
            response = client.post("/ai/chat", json={
                "prompt": "Hello from demo",
                "session_id": "demo-session"
            })
            
            assert response.status_code == 200
            data = response.json()
            assert "session_id" in data
            assert data["session_id"] == "demo-session"


class TestDemoResourceUpload:
    """Test resource upload endpoint for demo page"""
    
    def test_upload_endpoint_placeholder(self):
        """Placeholder test for /api/resources/upload endpoint"""
        # TODO: Implement when endpoint is created (issue #36)
        # This endpoint does not exist yet, documented for future implementation
        pass
    
    def test_upload_accepts_files(self):
        """Verify upload endpoint accepts file uploads"""
        # TODO: Implement when endpoint is created (issue #36)
        pass
    
    def test_upload_validates_file_types(self):
        """Verify upload endpoint validates file types"""
        # TODO: Implement when endpoint is created (issue #36)
        pass


class TestDemoIntegration:
    """Integration tests for demo page functionality"""
    
    def test_demo_end_to_end_chat_flow(self):
        """Test complete chat flow from demo page perspective"""
        # TODO: Implement full integration test (issue #36)
        # This would simulate user interaction with demo page
        pass
    
    def test_demo_handles_api_errors_gracefully(self):
        """Verify demo page handles API errors appropriately"""
        # TODO: Implement error handling tests (issue #36)
        pass
    
    def test_demo_session_management(self):
        """Verify demo page manages sessions correctly"""
        # TODO: Implement session management tests (issue #36)
        pass


# Smoke test to verify test file is loadable
def test_demo_tests_loadable():
    """Verify this test file can be loaded by pytest"""
    assert True, "Demo test file loaded successfully"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
