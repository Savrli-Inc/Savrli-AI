"""
Tests for Playground API endpoints

Test suite for playground session management endpoints.
"""

import pytest
from fastapi.testclient import TestClient
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Set environment variable before importing the app
os.environ['OPENAI_API_KEY'] = 'test-key-12345'

from api.index import app

client = TestClient(app)


class TestPlaygroundSessionCreation:
    """Test session creation endpoint"""
    
    def test_create_session_minimal(self):
        """Test creating a session with minimal parameters"""
        response = client.post("/api/playground/session", json={})
        assert response.status_code == 201
        data = response.json()
        assert "session_id" in data
        assert data["name"] == "Playground Session"  # default name
        assert data["message_count"] == 0
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_create_session_with_name(self):
        """Test creating a session with custom name"""
        response = client.post("/api/playground/session", json={
            "name": "Test Session"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Session"
        assert "session_id" in data
    
    def test_create_session_with_metadata(self):
        """Test creating a session with metadata"""
        response = client.post("/api/playground/session", json={
            "name": "Metadata Session",
            "metadata": {
                "user": "test_user",
                "project": "demo"
            }
        })
        assert response.status_code == 201
        data = response.json()
        assert data["metadata"]["user"] == "test_user"
        assert data["metadata"]["project"] == "demo"


class TestPlaygroundSessionRetrieval:
    """Test session retrieval endpoint"""
    
    def test_get_session_success(self):
        """Test retrieving an existing session"""
        # Create a session first
        create_response = client.post("/api/playground/session", json={
            "name": "Retrieve Test"
        })
        session_id = create_response.json()["session_id"]
        
        # Retrieve it
        response = client.get(f"/api/playground/session/{session_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == session_id
        assert data["name"] == "Retrieve Test"
    
    def test_get_session_not_found(self):
        """Test retrieving a non-existent session"""
        response = client.get("/api/playground/session/nonexistent-id")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestPlaygroundSessionDeletion:
    """Test session deletion endpoint"""
    
    def test_delete_session_success(self):
        """Test deleting an existing session"""
        # Create a session first
        create_response = client.post("/api/playground/session", json={
            "name": "Delete Test"
        })
        session_id = create_response.json()["session_id"]
        
        # Delete it
        response = client.delete(f"/api/playground/session/{session_id}")
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"].lower()
        
        # Verify it's gone
        get_response = client.get(f"/api/playground/session/{session_id}")
        assert get_response.status_code == 404
    
    def test_delete_session_not_found(self):
        """Test deleting a non-existent session"""
        response = client.delete("/api/playground/session/nonexistent-id")
        assert response.status_code == 404


class TestPlaygroundSessionListing:
    """Test session listing endpoint"""
    
    def test_list_sessions_empty(self):
        """Test listing when no sessions exist"""
        # Note: Other tests may have created sessions, so we can't guarantee empty
        response = client.get("/api/playground/sessions")
        assert response.status_code == 200
        data = response.json()
        assert "sessions" in data
        assert "total" in data
        assert "limit" in data
        assert "offset" in data
        assert isinstance(data["sessions"], list)
    
    def test_list_sessions_with_pagination(self):
        """Test listing sessions with pagination parameters"""
        # Create multiple sessions
        session_ids = []
        for i in range(3):
            response = client.post("/api/playground/session", json={
                "name": f"Session {i}"
            })
            session_ids.append(response.json()["session_id"])
        
        # List with limit
        response = client.get("/api/playground/sessions?limit=2&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert data["limit"] == 2
        assert data["offset"] == 0
        assert len(data["sessions"]) <= 2
        
        # Cleanup
        for session_id in session_ids:
            client.delete(f"/api/playground/session/{session_id}")
    
    def test_list_sessions_invalid_limit(self):
        """Test listing with invalid limit parameter"""
        response = client.get("/api/playground/sessions?limit=0")
        assert response.status_code == 422  # Validation error
    
    def test_list_sessions_limit_too_high(self):
        """Test listing with limit exceeding maximum"""
        response = client.get("/api/playground/sessions?limit=101")
        assert response.status_code == 422  # Validation error


class TestPlaygroundMessageCount:
    """Test message count update endpoint"""
    
    def test_update_message_count(self):
        """Test updating message count for a session"""
        # Create a session
        create_response = client.post("/api/playground/session", json={
            "name": "Message Count Test"
        })
        session_id = create_response.json()["session_id"]
        
        # Update message count
        response = client.put(
            f"/api/playground/session/{session_id}/message-count?count=5"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message_count"] == 5
        
        # Verify with get
        get_response = client.get(f"/api/playground/session/{session_id}")
        assert get_response.json()["message_count"] == 5
        
        # Cleanup
        client.delete(f"/api/playground/session/{session_id}")
    
    def test_update_message_count_not_found(self):
        """Test updating message count for non-existent session"""
        response = client.put(
            "/api/playground/session/nonexistent-id/message-count?count=5"
        )
        assert response.status_code == 404


class TestPlaygroundHealth:
    """Test playground health check endpoint"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/api/playground/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "active_sessions" in data
        assert "timestamp" in data
        assert isinstance(data["active_sessions"], int)
