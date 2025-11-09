"""
Base plugin interface and plugin manager for Savrli AI integrations.

This module provides the foundation for a plugin-style architecture
that allows third-party integrations with productivity platforms.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable
import logging

logger = logging.getLogger(__name__)


class Plugin(ABC):
    """
    Base class for all Savrli AI integration plugins.
    
    Each plugin represents an integration with a specific platform
    (e.g., Slack, Discord, Notion, Google Docs) and provides a
    standardized interface for sending messages and processing webhooks.
    """
    
    def __init__(self, ai_system: Any, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the plugin.
        
        Args:
            ai_system: Reference to the AI system for processing requests
            config: Optional configuration dictionary for the plugin
        """
        self.ai_system = ai_system
        self.config = config or {}
        self.enabled = self.config.get("enabled", True)
        self.name = self.__class__.__name__
    
    @abstractmethod
    def send_message(self, channel: str, message: str, **kwargs) -> Dict[str, Any]:
        """
        Send a message to the platform.
        
        Args:
            channel: Target channel/room/document identifier
            message: Message content to send
            **kwargs: Additional platform-specific parameters
            
        Returns:
            Dictionary with operation result including status and details
        """
        pass
    
    @abstractmethod
    def process_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming webhook from the platform.
        
        Args:
            webhook_data: Raw webhook payload from the platform
            
        Returns:
            Dictionary with processing result
        """
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """
        Validate plugin configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        pass
    
    def get_name(self) -> str:
        """Get the plugin name."""
        return self.name
    
    def is_enabled(self) -> bool:
        """Check if the plugin is enabled."""
        return self.enabled
    
    def enable(self):
        """Enable the plugin."""
        self.enabled = True
    
    def disable(self):
        """Disable the plugin."""
        self.enabled = False


class PluginManager:
    """
    Manager for all integration plugins.
    
    Handles plugin registration, lifecycle management, and routing
    of requests to appropriate plugins.
    """
    
    def __init__(self, ai_system: Any):
        """
        Initialize the plugin manager.
        
        Args:
            ai_system: Reference to the AI system
        """
        self.ai_system = ai_system
        self.plugins: Dict[str, Plugin] = {}
        self.webhook_handlers: Dict[str, Callable] = {}
    
    def register_plugin(self, plugin_name: str, plugin: Plugin) -> bool:
        """
        Register a new plugin.
        
        Args:
            plugin_name: Unique identifier for the plugin
            plugin: Plugin instance to register
            
        Returns:
            True if registration successful, False otherwise
        """
        if plugin_name in self.plugins:
            logger.warning(f"Plugin {plugin_name} already registered. Overwriting.")
        
        if not plugin.validate_config():
            logger.error(f"Plugin {plugin_name} configuration validation failed.")
            return False
        
        self.plugins[plugin_name] = plugin
        logger.info(f"Plugin {plugin_name} registered successfully.")
        return True
    
    def unregister_plugin(self, plugin_name: str) -> bool:
        """
        Unregister a plugin.
        
        Args:
            plugin_name: Name of the plugin to unregister
            
        Returns:
            True if unregistration successful, False if plugin not found
        """
        if plugin_name in self.plugins:
            del self.plugins[plugin_name]
            logger.info(f"Plugin {plugin_name} unregistered.")
            return True
        logger.warning(f"Plugin {plugin_name} not found for unregistration.")
        return False
    
    def get_plugin(self, plugin_name: str) -> Optional[Plugin]:
        """
        Get a registered plugin by name.
        
        Args:
            plugin_name: Name of the plugin to retrieve
            
        Returns:
            Plugin instance or None if not found
        """
        return self.plugins.get(plugin_name)
    
    def list_plugins(self) -> List[Dict[str, Any]]:
        """
        List all registered plugins.
        
        Returns:
            List of dictionaries containing plugin information
        """
        return [
            {
                "name": name,
                "enabled": plugin.is_enabled(),
                "class": plugin.__class__.__name__
            }
            for name, plugin in self.plugins.items()
        ]
    
    def send_message(self, plugin_name: str, channel: str, message: str, **kwargs) -> Dict[str, Any]:
        """
        Send a message via a specific plugin.
        
        Args:
            plugin_name: Name of the plugin to use
            channel: Target channel/location
            message: Message to send
            **kwargs: Additional platform-specific parameters
            
        Returns:
            Dictionary with operation result
        """
        plugin = self.get_plugin(plugin_name)
        if not plugin:
            return {
                "success": False,
                "error": f"Plugin {plugin_name} not found"
            }
        
        if not plugin.is_enabled():
            return {
                "success": False,
                "error": f"Plugin {plugin_name} is disabled"
            }
        
        try:
            result = plugin.send_message(channel, message, **kwargs)
            return {
                "success": True,
                "plugin": plugin_name,
                "result": result
            }
        except Exception as e:
            logger.exception(f"Error sending message via {plugin_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def process_webhook(self, plugin_name: str, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a webhook via a specific plugin.
        
        Args:
            plugin_name: Name of the plugin to use
            webhook_data: Webhook payload
            
        Returns:
            Dictionary with processing result
        """
        plugin = self.get_plugin(plugin_name)
        if not plugin:
            return {
                "success": False,
                "error": f"Plugin {plugin_name} not found"
            }
        
        if not plugin.is_enabled():
            return {
                "success": False,
                "error": f"Plugin {plugin_name} is disabled"
            }
        
        try:
            result = plugin.process_webhook(webhook_data)
            return {
                "success": True,
                "plugin": plugin_name,
                "result": result
            }
        except Exception as e:
            logger.exception(f"Error processing webhook via {plugin_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
