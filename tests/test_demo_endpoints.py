"""
Tests for demo page and endpoints.
This module contains comprehensive tests to verify that:
- The demo page loads correctly
- Static files are served
- Chat and upload endpoints work
- Integration with frontend is correct
"""
import pytest
import io
import sys
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Set dummy OpenAI key
os.environ['OPENAI_API_KEY'] = 'test-key-12345'

from api.index import app  # noqa: E402

client = TestClient(app)


class TestDemoPageEndpoint:
    """Test the /demo page endpoint"""

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
        assert "Chat API Demo" in content or "Chat" in content
        assert "chat-output" in content

    def test_demo_page_contains_upload_section(self):
        """Test that demo page contains upload demo section"""
        response = client.get("/demo")
        content = response.text
        assert "Upload" in content or "File" in content
        assert "upload-output" in content

    def test_demo_page_includes_demo_js(self):
        """Test that demo page includes demo.js script"""
        response = client.get("/demo")
        content = response.text
        assert "/static/js/demo.js" in content


class TestDemoJavaScriptFile:
    """Test that demo.js is accessible via static files"""

    def test_demo_js_accessible(self):
        """Test that demo.js file returns 200"""
        response = client.get("/static/js/demo.js")
        assert response.status_code == 200

    def test_demo_js_is_javascript(self):
        """Test that demo.js has correct content type"""
        response = client.get("/static/js/demo.js")
        ctype = response.headers["content-type"]
        assert any(
            mime in ctype for mime in
            ["javascript", "application/javascript", "text/javascript", "text/plain"]
        )

    def test_demo_js_contains_api_calls(self):
        """Test that demo.js contains expected API integration"""
        response = client.get("/static/js/demo.js")
        content = response.text
        assert "fetch" in content
        assert "/ai/chat" in content or "/api/resources/upload" in content


class TestResourceUploadEndpoint:
    """Test the /api/resources/upload endpoint"""

    def test_upload_endpoint_exists(self):
        """Test endpoint returns 422 without file (validation)"""
        response = client.post("/api/resources/upload")
        assert response.status_code == 422

    def test_upload_endpoint_accepts_file(self):
        """Test successful file upload"""
        test_file = io.BytesIO(b"test content")
        response = client.post(
            "/api/resources/upload",
            files={"file": ("test.txt", test_file, "text/plain")}
        )
        assert response.status_code == 200

    def test_upload_endpoint_returns_metadata(self):
        """Test metadata is returned correctly"""
        content = b"demo test file"
        test_file = io.BytesIO(content)
        response = client.post(
            "/api/resources/upload",
            files={"file": ("demo_test.txt", test_file, "text/plain")}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        file_info = data["file_info"]
        assert file_info["filename"] == "demo_test.txt"
        assert file_info["content_type"] == "text/plain"
        assert file_info["size"] == len(content)

    def test_upload_endpoint_handles_different_file_types(self):
        """Test multiple file types are accepted"""
        file_types = [
            ("test.txt", b"text", "text/plain"),
            ("data.json", b'{"key": "value"}', "application/json"),
            ("binary.bin", b"\x00\x01", "application/octet-stream"),
        ]
        for filename, content, ctype in file_types:
            test_file = io.BytesIO(content)
            response = client.post(
                "/api/resources/upload",
                files={"file": (filename, test_file, ctype)}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["file_info"]["filename"] == filename


class TestDemoPageIntegration:
    """Integration tests for demo page + JS"""

    def test_demo_page_chat_button_integration(self):
        """Test chat buttons have data-prompt"""
        response = client.get("/demo")
        content = response.text
        assert "data-prompt" in content
        assert "chat-demo-btn" in content

    def test_demo_page_form_elements(self):
        """Test custom chat form exists"""
        response = client.get("/demo")
        content = response.text
        assert "custom-chat-form" in content or "custom-prompt" in content
        assert "file-input" in content or 'type="file"' in content

    def test_demo_page_output_panels(self):
        """Test response containers exist"""
        response = client.get("/demo")
        content = response.text
        assert "chat-output" in content
        assert "upload-output" in content


class TestDemoEndpointsWithMocks:
    """Test endpoints with mocked OpenAI"""

    @patch('api.index.client.chat.completions.create')
    def test_chat_api_works_for_demo(self, mock_create):
        """Test chat endpoint with mock response"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Mocked AI response"
        mock_create.return_value = mock_response

        response = client.post("/ai/chat", json={"prompt": "Hello"})
        assert response.status_code == 200
        data = response.json()
        assert data["response"] == "Mocked AI response"

    @patch('api.index.client.chat.completions.create')
    def test_chat_endpoint_with_sample_prompts(self, mock_create):
        """Test multiple demo prompts"""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_create.return_value = mock_response

        prompts = [
            "What is the capital of France?",
            "Explain quantum computing",
            "Write a haiku about coding",
        ]
        for prompt in prompts:
            response = client.post("/ai/chat", json={"prompt": prompt})
            assert response.status_code == 200
            assert "response" in response.json()


class TestDemoDocumentation:
    """Test demo page includes docs links"""

    def test_demo_page_has_info_boxes(self):
        """Test informational sections"""
        response = client.get("/demo")
        content = response.text
        assert any(term in content for term in ["Endpoint:", "POST", "info-box"])

    def test_demo_page_links_to_docs(self):
        """Test links to documentation"""
        response = client.get("/demo")
        content = response.text
        assert any(link in content.lower() for link in ["docs", "documentation", "github"])
