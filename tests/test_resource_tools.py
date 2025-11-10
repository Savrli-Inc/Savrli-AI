"""
Tests for Resource Tools API endpoints.

This test module provides coverage for the resource management tools
including tagging, metadata, and import/export functionality.
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


class TestTagEndpoints:
    """Test tag management endpoints"""
    
    def test_add_tags(self):
        """Test adding tags to a resource"""
        response = client.post("/api/resource-tools/tags/add", json={
            "resource_id": "test-resource-1",
            "tags": ["customer-support", "high-priority"]
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["resource_id"] == "test-resource-1"
        assert "customer-support" in data["tags"]
        assert "high-priority" in data["tags"]
    
    def test_add_tags_empty_list(self):
        """Test adding empty tag list"""
        response = client.post("/api/resource-tools/tags/add", json={
            "resource_id": "test-resource-2",
            "tags": []
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["tags"] == []
    
    def test_remove_tags(self):
        """Test removing tags from a resource"""
        response = client.post("/api/resource-tools/tags/remove", json={
            "resource_id": "test-resource-1",
            "tags": ["high-priority"]
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["resource_id"] == "test-resource-1"
    
    def test_get_tags(self):
        """Test getting tags for a resource"""
        response = client.get("/api/resource-tools/tags/test-resource-1")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["resource_id"] == "test-resource-1"
        assert isinstance(data["tags"], list)
    
    def test_add_tags_missing_resource_id(self):
        """Test that missing resource_id is rejected"""
        response = client.post("/api/resource-tools/tags/add", json={
            "tags": ["test-tag"]
        })
        assert response.status_code == 422  # Validation error
    
    def test_add_tags_missing_tags(self):
        """Test that missing tags field is rejected"""
        response = client.post("/api/resource-tools/tags/add", json={
            "resource_id": "test-resource"
        })
        assert response.status_code == 422  # Validation error


class TestMetadataEndpoints:
    """Test metadata management endpoints"""
    
    def test_update_metadata(self):
        """Test updating metadata for a resource"""
        response = client.post("/api/resource-tools/metadata/update", json={
            "resource_id": "test-resource-1",
            "metadata": {
                "priority": "high",
                "region": "us-east",
                "department": "sales"
            }
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["resource_id"] == "test-resource-1"
        assert "priority" in data["metadata"]
        assert data["metadata"]["priority"] == "high"
        assert "updated_at" in data
    
    def test_update_metadata_empty(self):
        """Test updating with empty metadata"""
        response = client.post("/api/resource-tools/metadata/update", json={
            "resource_id": "test-resource-2",
            "metadata": {}
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["metadata"] == {}
    
    def test_get_metadata(self):
        """Test getting metadata for a resource"""
        response = client.get("/api/resource-tools/metadata/test-resource-1")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["resource_id"] == "test-resource-1"
        assert isinstance(data["metadata"], dict)
        assert "updated_at" in data
    
    def test_delete_metadata(self):
        """Test deleting metadata for a resource"""
        response = client.delete("/api/resource-tools/metadata/test-resource-1")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["resource_id"] == "test-resource-1"
    
    def test_delete_metadata_with_keys(self):
        """Test deleting specific metadata keys"""
        response = client.delete(
            "/api/resource-tools/metadata/test-resource-1?keys=priority&keys=region"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_update_metadata_missing_resource_id(self):
        """Test that missing resource_id is rejected"""
        response = client.post("/api/resource-tools/metadata/update", json={
            "metadata": {"key": "value"}
        })
        assert response.status_code == 422  # Validation error
    
    def test_update_metadata_missing_metadata(self):
        """Test that missing metadata field is rejected"""
        response = client.post("/api/resource-tools/metadata/update", json={
            "resource_id": "test-resource"
        })
        assert response.status_code == 422  # Validation error


class TestImportExportEndpoints:
    """Test import/export endpoints"""
    
    def test_import_resources(self):
        """Test importing resources"""
        response = client.post("/api/resource-tools/import", json={
            "source": "json",
            "data": '{"sessions": []}'
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["operation"] == "import"
        assert "count" in data
    
    def test_import_with_options(self):
        """Test importing with options"""
        response = client.post("/api/resource-tools/import", json={
            "source": "json",
            "data": '{"sessions": []}',
            "options": {
                "overwrite": False,
                "validate": True
            }
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_export_resources(self):
        """Test exporting resources"""
        response = client.post("/api/resource-tools/export", json={
            "resource_ids": ["session-1", "session-2"],
            "format": "json"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["operation"] == "export"
        assert data["count"] == 2
    
    def test_export_with_options(self):
        """Test exporting with options"""
        response = client.post("/api/resource-tools/export", json={
            "resource_ids": ["session-1"],
            "format": "csv",
            "options": {
                "include_metadata": True,
                "include_tags": True
            }
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["operation"] == "export"
    
    def test_export_empty_resource_list(self):
        """Test exporting with empty resource list"""
        response = client.post("/api/resource-tools/export", json={
            "resource_ids": [],
            "format": "json"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["count"] == 0
    
    def test_get_export_formats(self):
        """Test getting available export formats"""
        response = client.get("/api/resource-tools/export/formats")
        assert response.status_code == 200
        data = response.json()
        assert "formats" in data
        assert isinstance(data["formats"], list)
        assert "json" in data["formats"]
        assert "csv" in data["formats"]
    
    def test_get_import_sources(self):
        """Test getting available import sources"""
        response = client.get("/api/resource-tools/import/sources")
        assert response.status_code == 200
        data = response.json()
        assert "sources" in data
        assert isinstance(data["sources"], list)
        assert "json" in data["sources"]
    
    def test_import_missing_source(self):
        """Test that missing source is rejected"""
        response = client.post("/api/resource-tools/import", json={
            "data": '{"sessions": []}'
        })
        assert response.status_code == 422  # Validation error
    
    def test_import_missing_data(self):
        """Test that missing data is rejected"""
        response = client.post("/api/resource-tools/import", json={
            "source": "json"
        })
        assert response.status_code == 422  # Validation error
    
    def test_export_missing_resource_ids(self):
        """Test that missing resource_ids is rejected"""
        response = client.post("/api/resource-tools/export", json={
            "format": "json"
        })
        assert response.status_code == 422  # Validation error


class TestEndpointIntegration:
    """Test integration between endpoints"""
    
    def test_workflow_add_tags_and_metadata(self):
        """Test workflow: add tags, then metadata to same resource"""
        resource_id = "workflow-test-1"
        
        # Add tags
        tag_response = client.post("/api/resource-tools/tags/add", json={
            "resource_id": resource_id,
            "tags": ["test-workflow"]
        })
        assert tag_response.status_code == 200
        
        # Add metadata
        metadata_response = client.post("/api/resource-tools/metadata/update", json={
            "resource_id": resource_id,
            "metadata": {"test": "workflow"}
        })
        assert metadata_response.status_code == 200
        
        # Both should succeed
        assert tag_response.json()["success"] is True
        assert metadata_response.json()["success"] is True
    
    def test_workflow_export_after_tagging(self):
        """Test workflow: tag resources, then export them"""
        resource_id = "export-test-1"
        
        # Add tags
        client.post("/api/resource-tools/tags/add", json={
            "resource_id": resource_id,
            "tags": ["export-ready"]
        })
        
        # Export
        export_response = client.post("/api/resource-tools/export", json={
            "resource_ids": [resource_id],
            "format": "json"
        })
        assert export_response.status_code == 200
        assert export_response.json()["success"] is True


class TestResponseModels:
    """Test response model structure and consistency"""
    
    def test_tag_response_structure(self):
        """Test that tag responses have correct structure"""
        response = client.get("/api/resource-tools/tags/test-resource")
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        assert "success" in data
        assert "resource_id" in data
        assert "tags" in data
        assert isinstance(data["success"], bool)
        assert isinstance(data["tags"], list)
    
    def test_metadata_response_structure(self):
        """Test that metadata responses have correct structure"""
        response = client.get("/api/resource-tools/metadata/test-resource")
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        assert "success" in data
        assert "resource_id" in data
        assert "metadata" in data
        assert "updated_at" in data
        assert isinstance(data["success"], bool)
        assert isinstance(data["metadata"], dict)
    
    def test_import_export_response_structure(self):
        """Test that import/export responses have correct structure"""
        response = client.post("/api/resource-tools/export", json={
            "resource_ids": ["test"],
            "format": "json"
        })
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        assert "success" in data
        assert "operation" in data
        assert "count" in data
        assert isinstance(data["success"], bool)
        assert isinstance(data["count"], int)
