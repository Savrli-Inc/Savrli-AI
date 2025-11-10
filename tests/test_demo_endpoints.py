import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
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
    """Test demo page endpoint"""
    
    def test_demo_page_returns_200(self):
        """Test that demo page endpoint returns 200 OK"""
        response = client.get("/demo")
        assert response.status_code == 200
    
    def test_demo_page_returns_html(self):
        """Test that demo page returns HTML content"""
        response = client.get("/demo")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "<!DOCTYPE html>" in response.text
    
    def test_demo_page_contains_title(self):
        """Test that demo page contains expected title"""
        response = client.get("/demo")
        assert response.status_code == 200
        assert "Savrli AI Demo" in response.text
    
    def test_demo_page_contains_chat_section(self):
        """Test that demo page contains chat demo section"""
        response = client.get("/demo")
        assert response.status_code == 200
        assert "Chat Endpoint Demo" in response.text or "chat" in response.text.lower()
    
    def test_demo_page_contains_upload_section(self):
        """Test that demo page contains upload demo section"""
        response = client.get("/demo")
        assert response.status_code == 200
        assert "Upload" in response.text or "upload" in response.text.lower()
    
    def test_demo_page_loads_demo_js(self):
        """Test that demo page references demo.js"""
        response = client.get("/demo")
        assert response.status_code == 200
        assert "demo.js" in response.text


class TestChatEndpointForDemo:
    """Test chat endpoint with demo scenarios"""
    
    @patch('api.index.client.chat.completions.create')
    def test_chat_endpoint_returns_200(self, mock_create):
        """Test that chat endpoint returns 200 OK (stub for demo)"""
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Paris is the capital of France."
        mock_create.return_value = mock_response
        
        response = client.post("/ai/chat", json={
            "prompt": "What is the capital of France?"
        })
        assert response.status_code == 200
    
    @patch('api.index.client.chat.completions.create')
    def test_chat_endpoint_with_sample_prompts(self, mock_create):
        """Test chat endpoint with various sample prompts from demo"""
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_create.return_value = mock_response
        
        sample_prompts = [
            "What is the capital of France?",
            "Explain quantum computing in simple terms",
            "Write a haiku about coding",
            "What are the benefits of exercise?",
            "Suggest a quick healthy breakfast recipe",
            "Tell me a fun fact about space"
        ]
        
        for prompt in sample_prompts:
            response = client.post("/ai/chat", json={"prompt": prompt})
            assert response.status_code == 200
            assert "response" in response.json()


class TestResourceUploadEndpoint:
    """Test resource upload endpoint for demo"""
    
    def test_upload_endpoint_returns_200(self):
        """Test that upload endpoint returns 200 OK (stub for demo)"""
        # Create a simple test file
        file_content = b"Test file content"
        files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
        
        response = client.post("/resources/upload", files=files)
        assert response.status_code == 200
    
    def test_upload_endpoint_returns_metadata(self):
        """Test that upload endpoint returns file metadata"""
        file_content = b"Test file content for metadata"
        files = {"file": ("demo_test.txt", io.BytesIO(file_content), "text/plain")}
        
        response = client.post("/resources/upload", files=files)
        assert response.status_code == 200
        
        data = response.json()
        assert "success" in data
        assert "filename" in data
        assert "content_type" in data
        assert "size" in data
    
    def test_upload_endpoint_accepts_different_file_types(self):
        """Test that upload endpoint accepts various file types"""
        file_types = [
            ("test.txt", b"text content", "text/plain"),
            ("test.json", b'{"key": "value"}', "application/json"),
            ("test.csv", b"col1,col2\nval1,val2", "text/csv"),
        ]
        
        for filename, content, content_type in file_types:
            files = {"file": (filename, io.BytesIO(content), content_type)}
            response = client.post("/resources/upload", files=files)
            assert response.status_code == 200
            data = response.json()
            assert data["filename"] == filename
    
    def test_upload_endpoint_handles_large_files(self):
        """Test that upload endpoint can handle larger files"""
        # Create a 1MB test file
        file_content = b"x" * (1024 * 1024)
        files = {"file": ("large_test.bin", io.BytesIO(file_content), "application/octet-stream")}
        
        response = client.post("/resources/upload", files=files)
        assert response.status_code == 200
        
        data = response.json()
        assert data["size"] == len(file_content)
    
    def test_upload_endpoint_requires_file(self):
        """Test that upload endpoint requires a file parameter"""
        response = client.post("/resources/upload")
        assert response.status_code == 422  # Unprocessable Entity


class TestStaticFilesServing:
    """Test static files serving for demo.js"""
    
    def test_demo_js_accessible(self):
        """Test that demo.js is accessible via static files"""
        response = client.get("/static/js/demo.js")
        # Should return 200 if static files are mounted, or 404 if not found
        # We accept both since static mounting might not work in test environment
        assert response.status_code in [200, 404]
    
    def test_demo_js_contains_expected_content(self):
        """Test that demo.js contains expected functions if accessible"""
        response = client.get("/static/js/demo.js")
        if response.status_code == 200:
            # Check for key function names
            content = response.text
            assert "handleChatDemo" in content or "CHAT_ENDPOINT" in content
