import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os
import sys
import json

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Set environment variable before importing the app
os.environ['OPENAI_API_KEY'] = 'test-key-12345'

from api.index import app, conversation_history

client = TestClient(app)


class TestSessionListing:
    """Test session listing endpoints"""
    
    def setup_method(self):
        """Setup test data before each test"""
        conversation_history.clear()
        # Add test sessions
        conversation_history["session1"] = [
            {"role": "user", "content": "Hello", "timestamp": "2025-01-01T10:00:00Z"},
            {"role": "assistant", "content": "Hi there!", "timestamp": "2025-01-01T10:00:01Z"}
        ]
        conversation_history["session2"] = [
            {"role": "user", "content": "Test", "timestamp": "2025-01-01T11:00:00Z"},
            {"role": "assistant", "content": "Response", "timestamp": "2025-01-01T11:00:01Z"},
            {"role": "user", "content": "More", "timestamp": "2025-01-01T11:00:02Z"},
        ]
    
    def teardown_method(self):
        """Clean up after each test"""
        conversation_history.clear()
    
    def test_list_all_sessions(self):
        """Test listing all sessions"""
        response = client.get("/ai/sessions")
        assert response.status_code == 200
        data = response.json()
        assert "sessions" in data
        assert data["count"] == 2
        assert data["total_sessions"] == 2
    
    def test_list_sessions_min_messages(self):
        """Test filtering by minimum messages"""
        response = client.get("/ai/sessions?min_messages=3")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1  # Only session2 has 3 messages
    
    def test_list_sessions_max_messages(self):
        """Test filtering by maximum messages"""
        response = client.get("/ai/sessions?max_messages=2")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1  # Only session1 has 2 messages
    
    def test_get_session_stats(self):
        """Test getting session statistics"""
        response = client.get("/ai/sessions/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_sessions"] == 2
        assert data["total_messages"] == 5
        assert "average_messages_per_session" in data
        assert "largest_session" in data
        assert "smallest_session" in data


class TestSessionExport:
    """Test session export functionality"""
    
    def setup_method(self):
        """Setup test data before each test"""
        conversation_history.clear()
        conversation_history["test_session"] = [
            {"role": "user", "content": "Hello", "timestamp": "2025-01-01T10:00:00Z"},
            {"role": "assistant", "content": "Hi!", "timestamp": "2025-01-01T10:00:01Z"}
        ]
    
    def teardown_method(self):
        """Clean up after each test"""
        conversation_history.clear()
    
    def test_export_json(self):
        """Test exporting session as JSON"""
        response = client.post("/ai/sessions/export", json={
            "session_id": "test_session",
            "format": "json"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["format"] == "json"
        assert data["message_count"] == 2
        assert "data" in data
        
        # Verify JSON is valid
        exported = json.loads(data["data"])
        assert len(exported) == 2
        assert exported[0]["role"] == "user"
    
    def test_export_csv(self):
        """Test exporting session as CSV"""
        response = client.post("/ai/sessions/export", json={
            "session_id": "test_session",
            "format": "csv"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["format"] == "csv"
        assert "role,content,timestamp" in data["data"]
    
    def test_export_markdown(self):
        """Test exporting session as Markdown"""
        response = client.post("/ai/sessions/export", json={
            "session_id": "test_session",
            "format": "markdown"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["format"] == "markdown"
        assert "# Conversation History" in data["data"]
    
    def test_export_invalid_format(self):
        """Test exporting with invalid format"""
        response = client.post("/ai/sessions/export", json={
            "session_id": "test_session",
            "format": "xml"
        })
        assert response.status_code == 400
    
    def test_export_nonexistent_session(self):
        """Test exporting non-existent session"""
        response = client.post("/ai/sessions/export", json={
            "session_id": "nonexistent",
            "format": "json"
        })
        assert response.status_code == 404


class TestSessionImport:
    """Test session import functionality"""
    
    def teardown_method(self):
        """Clean up after each test"""
        conversation_history.clear()
    
    def test_import_json(self):
        """Test importing session from JSON"""
        json_data = json.dumps([
            {"role": "user", "content": "Imported message 1"},
            {"role": "assistant", "content": "Imported response 1"}
        ])
        
        response = client.post("/ai/sessions/import", json={
            "session_id": "imported_session",
            "format": "json",
            "data": json_data
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["imported_message_count"] == 2
        
        # Verify import worked
        assert "imported_session" in conversation_history
        assert len(conversation_history["imported_session"]) == 2
    
    def test_import_csv(self):
        """Test importing session from CSV"""
        csv_data = """role,content,timestamp
user,Hello,2025-01-01T10:00:00Z
assistant,Hi!,2025-01-01T10:00:01Z"""
        
        response = client.post("/ai/sessions/import", json={
            "session_id": "csv_imported",
            "format": "csv",
            "data": csv_data
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["imported_message_count"] == 2
    
    def test_import_invalid_json(self):
        """Test importing invalid JSON"""
        response = client.post("/ai/sessions/import", json={
            "session_id": "test",
            "format": "json",
            "data": "not valid json"
        })
        assert response.status_code == 400
    
    def test_import_invalid_format(self):
        """Test importing with invalid format"""
        response = client.post("/ai/sessions/import", json={
            "session_id": "test",
            "format": "xml",
            "data": "<xml></xml>"
        })
        assert response.status_code == 400


class TestBulkOperations:
    """Test bulk session operations"""
    
    def setup_method(self):
        """Setup test data before each test"""
        conversation_history.clear()
        for i in range(5):
            conversation_history[f"session{i}"] = [
                {"role": "user", "content": f"Message {i}"}
            ]
    
    def teardown_method(self):
        """Clean up after each test"""
        conversation_history.clear()
    
    def test_bulk_delete(self):
        """Test deleting multiple sessions"""
        response = client.request(
            method="DELETE",
            url="/ai/sessions/bulk",
            json={"session_ids": ["session0", "session1", "session2"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["deleted_count"] == 3
        assert len(conversation_history) == 2
    
    def test_bulk_delete_with_nonexistent(self):
        """Test bulk delete with some non-existent sessions"""
        response = client.request(
            method="DELETE",
            url="/ai/sessions/bulk",
            json={"session_ids": ["session0", "nonexistent1", "session1", "nonexistent2"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["deleted_count"] == 2
        assert data["not_found_count"] == 2
    
    def test_clear_all_sessions(self):
        """Test clearing all sessions"""
        response = client.delete("/ai/sessions/all")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["cleared_count"] == 5
        assert len(conversation_history) == 0


class TestResourceManagerModule:
    """Test resource_manager module directly"""
    
    def test_conversation_exporter_json(self):
        """Test ConversationExporter.to_json"""
        from resource_manager import ConversationExporter
        
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi!"}
        ]
        
        result = ConversationExporter.to_json(messages)
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert len(parsed) == 2
    
    def test_conversation_exporter_csv(self):
        """Test ConversationExporter.to_csv"""
        from resource_manager import ConversationExporter
        
        messages = [
            {"role": "user", "content": "Hello", "timestamp": "2025-01-01T10:00:00Z"},
            {"role": "assistant", "content": "Hi!", "timestamp": "2025-01-01T10:00:01Z"}
        ]
        
        result = ConversationExporter.to_csv(messages)
        assert "role,content,timestamp" in result
        assert "user,Hello" in result
    
    def test_conversation_importer_json(self):
        """Test ConversationImporter.from_json"""
        from resource_manager import ConversationImporter
        
        json_data = json.dumps([
            {"role": "user", "content": "Test"}
        ])
        
        result = ConversationImporter.from_json(json_data)
        assert len(result) == 1
        assert result[0]["role"] == "user"
    
    def test_conversation_importer_invalid_json(self):
        """Test ConversationImporter with invalid JSON"""
        from resource_manager import ConversationImporter
        
        with pytest.raises(ValueError):
            ConversationImporter.from_json("not json")
    
    def test_session_manager_list_sessions(self):
        """Test SessionManager.list_sessions"""
        from resource_manager import SessionManager
        from collections import defaultdict
        
        test_history = defaultdict(list)
        test_history["s1"] = [{"role": "user", "content": "1"}]
        test_history["s2"] = [{"role": "user", "content": "2"}, {"role": "assistant", "content": "2"}]
        
        manager = SessionManager(test_history)
        sessions = manager.list_sessions()
        
        assert len(sessions) == 2
        assert all("session_id" in s for s in sessions)
        assert all("message_count" in s for s in sessions)
