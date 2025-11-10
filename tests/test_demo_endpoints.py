"""
Tests for demo page and endpoints.

This module contains basic tests to verify that the demo page and 
its associated endpoints are accessible and return expected responses.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import os
import sys
import io

# Add parent directory to path to import the API
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Set environment variable before importing the app
os.environ['OPENAI_API_KEY'] = 'test-key-12345'

from api.index import app

client = TestClient(app)


class TestDemoPageEndpoint:
    """Test the demo page endpoint"""
    
    def test_demo_page_returns_200(self):
        """Test that demo page endpoint returns 200 OK"""
        response = client.get("/demo")
        assert response.status_code == 200
    
    def test_demo_page_returns_html(self):
        """Test that demo page returns HTML content"""
        response = client.get("/demo")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"
    
    def test_demo_page_contains_title(self):
        """Test that demo page contains expected title"""
        response = client.get("/demo")
        content = response.text
        assert "Savrli AI Demo" in content
    
    def test_demo_page_contains_chat_section(self):
        """Test that demo page contains chat API demo section"""
        response = client.get("/demo")
        content = response.text
        assert "Chat API Demo" in content
        assert "chat-output" in content
    
    def test_demo_page_contains_upload_section(self):
        """Test that demo page contains upload demo section"""
        response = client.get("/demo")
        content = response.text
        assert "Upload" in content or "upload" in content
        assert "upload-output" in content
    
    def test_demo_page_includes_demo_js(self):
        """Test that demo page includes demo.js script"""
        response = client.get("/demo")
        content = response.text
        assert "/static/js/demo.js" in content or "demo.js" in content


class TestDemoJavaScriptFile:
    """Test that demo.js is accessible"""
    
    def test_demo_js_accessible(self):
        """Test that demo.js file is accessible via static files"""
        response = client.get("/static/js/demo.js")
        assert response.status_code == 200
    
    def test_demo_js_is_javascript(self):
        """Test that demo.js has correct content type"""
        response = client.get("/static/js/demo.js")
        # Accept various JavaScript MIME types
        assert "javascript" in response.headers["content-type"] or \
               "application/javascript" in response.headers["content-type"] or \
               response.headers["content-type"] == "text/plain"
    
    def test_demo_js_contains_api_calls(self):
        """Test that demo.js contains API integration code"""
        response = client.get("/static/js/demo.js")
        content = response.text
        assert "callChatAPI" in content or "fetch" in content
        assert "/ai/chat" in content


class TestResourceUploadEndpoint:
    """Test the /api/resources/upload endpoint"""
    
    def test_upload_endpoint_exists(self):
        """Test that upload endpoint exists and returns expected error without file"""
        response = client.post("/api/resources/upload")
        # Should return 422 for missing required file parameter
        assert response.status_code == 422
    
    def test_upload_endpoint_accepts_file(self):
        """Test that upload endpoint accepts file uploads"""
        # Create a test file
        test_file = io.BytesIO(b"test file content")
        
        response = client.post(
            "/api/resources/upload",
            files={"file": ("test.txt", test_file, "text/plain")}
        )
        
        assert response.status_code == 200
    
    def test_upload_endpoint_returns_metadata(self):
        """Test that upload endpoint returns file metadata"""
        test_content = b"test file content for demo"
        test_file = io.BytesIO(test_content)
        
        response = client.post(
            "/api/resources/upload",
            files={"file": ("demo_test.txt", test_file, "text/plain")}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "success" in data
        assert data["success"] is True
        assert "file_info" in data
        assert data["file_info"]["filename"] == "demo_test.txt"
        assert data["file_info"]["content_type"] == "text/plain"
        assert data["file_info"]["size"] == len(test_content)
    
    def test_upload_endpoint_handles_different_file_types(self):
        """Test that upload endpoint handles various file types"""
        file_types = [
            ("test.txt", b"text content", "text/plain"),
            ("test.json", b'{"key": "value"}', "application/json"),
            ("test.bin", b"\x00\x01\x02\x03", "application/octet-stream"),
        ]
        
        for filename, content, content_type in file_types:
            test_file = io.BytesIO(content)
            response = client.post(
                "/api/resources/upload",
                files={"file": (filename, test_file, content_type)}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["file_info"]["filename"] == filename


class TestDemoPageIntegration:
    """Integration tests for demo page functionality"""
    
    def test_demo_page_chat_button_integration(self):
        """Test that demo page chat buttons have correct data attributes"""
        response = client.get("/demo")
        content = response.text
        
        # Check for button with data-prompt attribute
        assert "data-prompt" in content
        assert "chat-demo-btn" in content
    
    def test_demo_page_form_elements(self):
        """Test that demo page contains necessary form elements"""
        response = client.get("/demo")
        content = response.text
        
        # Check for custom chat form
        assert "custom-chat-form" in content
        assert "custom-prompt" in content
        
        # Check for file upload input
        assert "file-input" in content
        assert 'type="file"' in content
    
    def test_demo_page_output_panels(self):
        """Test that demo page contains output panels for responses"""
        response = client.get("/demo")
        content = response.text
        
        assert "chat-output" in content
        assert "upload-output" in content


class TestDemoEndpointsWithMocks:
    """Test demo endpoints with mocked AI responses"""
    
    @patch('api.index.client.chat.completions.create')
    def test_chat_api_works_for_demo(self, mock_create):
        """Test that chat API works for demo page usage"""
        from unittest.mock import MagicMock
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Demo response"
        mock_create.return_value = mock_response
        
        response = client.post("/ai/chat", json={"prompt": "Hello from demo"})
        assert response.status_code == 200
        assert "response" in response.json()


class TestDemoDocumentation:
    """Test demo-related documentation"""
    
    def test_demo_page_has_info_boxes(self):
        """Test that demo page has informational boxes"""
        response = client.get("/demo")
        content = response.text
        
        assert "info-box" in content
        assert "Endpoint:" in content
        assert "/ai/chat" in content
    
    def test_demo_page_links_to_docs(self):
        """Test that demo page links to documentation"""
        response = client.get("/demo")
        content = response.text
        
        assert "Documentation" in content or "docs" in content.lower()
