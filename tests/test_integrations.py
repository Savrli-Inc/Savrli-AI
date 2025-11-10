"""
Tests for integration plugins and plugin manager.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Set environment variable before importing
os.environ['OPENAI_API_KEY'] = 'test-key-12345'

from api.index import app
from integrations.plugin_base import Plugin, PluginManager
from integrations.slack_plugin import SlackPlugin
from integrations.discord_plugin import DiscordPlugin
from integrations.notion_plugin import NotionPlugin
from integrations.google_docs_plugin import GoogleDocsPlugin

client = TestClient(app)


class TestPluginBase:
    """Test base plugin functionality"""
    
    def test_plugin_manager_initialization(self):
        """Test plugin manager initializes correctly"""
        ai_system = MagicMock()
        manager = PluginManager(ai_system)
        
        assert manager.ai_system == ai_system
        assert isinstance(manager.plugins, dict)
        assert len(manager.plugins) == 0
    
    def test_plugin_registration(self):
        """Test registering a plugin"""
        ai_system = MagicMock()
        manager = PluginManager(ai_system)
        
        config = {"bot_token": "test-token", "signing_secret": "test-secret"}
        plugin = SlackPlugin(ai_system, config)
        
        result = manager.register_plugin("test_slack", plugin)
        assert result is True
        assert "test_slack" in manager.plugins
    
    def test_plugin_unregistration(self):
        """Test unregistering a plugin"""
        ai_system = MagicMock()
        manager = PluginManager(ai_system)
        
        config = {"bot_token": "test-token", "signing_secret": "test-secret"}
        plugin = SlackPlugin(ai_system, config)
        manager.register_plugin("test_slack", plugin)
        
        result = manager.unregister_plugin("test_slack")
        assert result is True
        assert "test_slack" not in manager.plugins
    
    def test_list_plugins(self):
        """Test listing registered plugins"""
        ai_system = MagicMock()
        manager = PluginManager(ai_system)
        
        config = {"bot_token": "test-token", "signing_secret": "test-secret"}
        plugin = SlackPlugin(ai_system, config)
        manager.register_plugin("test_slack", plugin)
        
        plugins = manager.list_plugins()
        assert len(plugins) == 1
        assert plugins[0]["name"] == "test_slack"
        assert plugins[0]["enabled"] is True


class TestSlackPlugin:
    """Test Slack integration plugin"""
    
    def test_slack_plugin_initialization(self):
        """Test Slack plugin initializes correctly"""
        ai_system = MagicMock()
        config = {"bot_token": "test-token", "signing_secret": "test-secret"}
        plugin = SlackPlugin(ai_system, config)
        
        assert plugin.ai_system == ai_system
        assert plugin.bot_token == "test-token"
        assert plugin.signing_secret == "test-secret"
    
    def test_slack_validate_config_success(self):
        """Test Slack config validation succeeds with valid config"""
        ai_system = MagicMock()
        config = {"bot_token": "test-token", "signing_secret": "test-secret"}
        plugin = SlackPlugin(ai_system, config)
        
        assert plugin.validate_config() is True
    
    def test_slack_validate_config_failure(self):
        """Test Slack config validation fails with missing config"""
        ai_system = MagicMock()
        config = {}
        plugin = SlackPlugin(ai_system, config)
        
        assert plugin.validate_config() is False
    
    def test_slack_send_message(self):
        """Test sending a message via Slack plugin"""
        ai_system = MagicMock()
        config = {"bot_token": "test-token", "signing_secret": "test-secret"}
        plugin = SlackPlugin(ai_system, config)
        
        result = plugin.send_message("C1234567890", "Test message")
        
        assert result["status"] == "success"
        assert result["channel"] == "C1234567890"
        assert result["message"] == "Test message"
    
    def test_slack_process_webhook_url_verification(self):
        """Test Slack URL verification challenge"""
        ai_system = MagicMock()
        config = {"bot_token": "test-token", "signing_secret": "test-secret"}
        plugin = SlackPlugin(ai_system, config)
        
        webhook_data = {
            "type": "url_verification",
            "challenge": "test-challenge-123"
        }
        
        result = plugin.process_webhook(webhook_data)
        assert result["status"] == "success"
        assert result["challenge"] == "test-challenge-123"
    
    def test_slack_process_webhook_message_event(self):
        """Test processing Slack message event"""
        ai_system = MagicMock()
        config = {"bot_token": "test-token", "signing_secret": "test-secret"}
        plugin = SlackPlugin(ai_system, config)
        
        webhook_data = {
            "type": "event_callback",
            "event": {
                "type": "message",
                "text": "Hello bot",
                "channel": "C1234567890",
                "user": "U1234567890"
            }
        }
        
        result = plugin.process_webhook(webhook_data)
        assert result["status"] == "success"
        assert result["event_type"] == "message"


class TestDiscordPlugin:
    """Test Discord integration plugin"""
    
    def test_discord_plugin_initialization(self):
        """Test Discord plugin initializes correctly"""
        ai_system = MagicMock()
        config = {"bot_token": "test-token", "application_id": "test-app-id"}
        plugin = DiscordPlugin(ai_system, config)
        
        assert plugin.ai_system == ai_system
        assert plugin.bot_token == "test-token"
        assert plugin.application_id == "test-app-id"
    
    def test_discord_send_message(self):
        """Test sending a message via Discord plugin"""
        ai_system = MagicMock()
        config = {"bot_token": "test-token", "application_id": "test-app-id"}
        plugin = DiscordPlugin(ai_system, config)
        
        result = plugin.send_message("123456789", "Test message")
        
        assert result["status"] == "success"
        assert result["channel"] == "123456789"
        assert result["message"] == "Test message"
    
    def test_discord_process_webhook_ping(self):
        """Test Discord PING interaction"""
        ai_system = MagicMock()
        config = {"bot_token": "test-token", "application_id": "test-app-id"}
        plugin = DiscordPlugin(ai_system, config)
        
        webhook_data = {"type": 1}  # PING
        
        result = plugin.process_webhook(webhook_data)
        assert result["type"] == 1  # PONG
        assert result["status"] == "success"
    
    def test_discord_process_webhook_command(self):
        """Test Discord slash command"""
        ai_system = MagicMock()
        config = {"bot_token": "test-token", "application_id": "test-app-id"}
        plugin = DiscordPlugin(ai_system, config)
        
        webhook_data = {
            "type": 2,  # APPLICATION_COMMAND
            "data": {
                "name": "help"
            }
        }
        
        result = plugin.process_webhook(webhook_data)
        assert result["type"] == 4  # CHANNEL_MESSAGE_WITH_SOURCE
        assert result["status"] == "success"


class TestNotionPlugin:
    """Test Notion integration plugin"""
    
    def test_notion_plugin_initialization(self):
        """Test Notion plugin initializes correctly"""
        ai_system = MagicMock()
        config = {"api_token": "test-token"}
        plugin = NotionPlugin(ai_system, config)
        
        assert plugin.ai_system == ai_system
        assert plugin.api_token == "test-token"
    
    def test_notion_send_message_create_page(self):
        """Test creating a page via Notion plugin"""
        ai_system = MagicMock()
        config = {"api_token": "test-token"}
        plugin = NotionPlugin(ai_system, config)
        
        result = plugin.send_message(
            "page-id-123",
            "Test content",
            operation="create_page",
            properties={"title": "Test Page"}
        )
        
        assert result["status"] == "success"
        assert result["operation"] == "create_page"
        assert result["page_id"] == "page-id-123"
    
    def test_notion_search_pages(self):
        """Test searching Notion pages"""
        ai_system = MagicMock()
        config = {"api_token": "test-token"}
        plugin = NotionPlugin(ai_system, config)
        
        result = plugin.search_pages("test query")
        
        assert result["status"] == "success"
        assert result["query"] == "test query"


class TestGoogleDocsPlugin:
    """Test Google Docs integration plugin"""
    
    def test_google_docs_plugin_initialization(self):
        """Test Google Docs plugin initializes correctly"""
        ai_system = MagicMock()
        config = {"credentials": "test-credentials"}
        plugin = GoogleDocsPlugin(ai_system, config)
        
        assert plugin.ai_system == ai_system
        assert plugin.credentials == "test-credentials"
    
    def test_google_docs_send_message_create_document(self):
        """Test creating a document via Google Docs plugin"""
        ai_system = MagicMock()
        config = {"credentials": "test-credentials"}
        plugin = GoogleDocsPlugin(ai_system, config)
        
        result = plugin.send_message(
            "new",
            "Test content",
            operation="create_document",
            title="Test Document"
        )
        
        assert result["status"] == "success"
        assert result["operation"] == "create_document"
        assert result["title"] == "Test Document"
    
    def test_google_docs_send_message_append_text(self):
        """Test appending text to a document"""
        ai_system = MagicMock()
        config = {"credentials": "test-credentials"}
        plugin = GoogleDocsPlugin(ai_system, config)
        
        result = plugin.send_message(
            "doc-id-123",
            "Test content",
            operation="append_text",
            index=1
        )
        
        assert result["status"] == "success"
        assert result["operation"] == "append_text"
        assert result["document_id"] == "doc-id-123"
    
    def test_google_docs_get_document(self):
        """Test getting document content"""
        ai_system = MagicMock()
        config = {"credentials": "test-credentials"}
        plugin = GoogleDocsPlugin(ai_system, config)
        
        result = plugin.get_document("doc-id-123")
        
        assert result["status"] == "success"
        assert result["document_id"] == "doc-id-123"


class TestIntegrationEndpoints:
    """Test integration API endpoints"""
    
    def test_list_integrations(self):
        """Test listing available integrations"""
        response = client.get("/integrations")
        
        assert response.status_code == 200
        data = response.json()
        assert "integrations" in data
        assert "count" in data
        assert isinstance(data["integrations"], list)
    
    def test_get_integration_info_not_found(self):
        """Test getting info for non-existent plugin"""
        response = client.get("/integrations/nonexistent/info")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
