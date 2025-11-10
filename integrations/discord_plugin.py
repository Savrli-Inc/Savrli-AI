"""
Discord integration plugin for Savrli AI.

This plugin enables sending messages to Discord channels and processing
incoming Discord webhooks/events.
"""

from typing import Dict, Any, Optional
import logging
from .plugin_base import Plugin

logger = logging.getLogger(__name__)


class DiscordPlugin(Plugin):
    """
    Discord integration plugin.
    
    Provides functionality to send messages to Discord channels and
    process incoming Discord events via webhooks.
    
    Configuration keys:
        - bot_token: Discord bot token for authentication
        - application_id: Discord application ID
        - public_key: Discord public key for webhook verification
        - enabled: Whether the plugin is enabled (default: True)
    """
    
    def __init__(self, ai_system: Any, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Discord plugin.
        
        Args:
            ai_system: Reference to the AI system
            config: Configuration dictionary with Discord credentials
        """
        super().__init__(ai_system, config)
        self.bot_token = self.config.get("bot_token")
        self.application_id = self.config.get("application_id")
        self.public_key = self.config.get("public_key")
    
    def validate_config(self) -> bool:
        """
        Validate Discord configuration.
        
        Returns:
            True if configuration is valid
        """
        if not self.bot_token:
            logger.warning("Discord bot_token not configured")
            return False
        if not self.application_id:
            logger.warning("Discord application_id not configured")
            return False
        return True
    
    def send_message(self, channel: str, message: str, **kwargs) -> Dict[str, Any]:
        """
        Send a message to a Discord channel.
        
        Args:
            channel: Discord channel ID
            message: Message text to send
            **kwargs: Additional Discord API parameters:
                - embed: Rich embed object
                - tts: Text-to-speech flag
                - allowed_mentions: Allowed mentions configuration
                
        Returns:
            Dictionary with operation result
        """
        # In a production implementation, this would use the Discord SDK
        # For now, return a structured response indicating the operation
        
        if not self.is_enabled():
            return {
                "status": "error",
                "error": "Discord plugin is disabled"
            }
        
        # Simulate sending message
        logger.info(f"Discord: Sending message to channel {channel}")
        
        return {
            "status": "success",
            "channel": channel,
            "message": message,
            "embed": kwargs.get("embed"),
            "tts": kwargs.get("tts", False),
            "note": "Production implementation would use Discord SDK (discord.py)"
        }
    
    def process_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming Discord webhook/interaction.
        
        Args:
            webhook_data: Discord interaction payload
            
        Returns:
            Dictionary with processing result
        """
        if not self.is_enabled():
            return {
                "status": "error",
                "error": "Discord plugin is disabled"
            }
        
        # Handle different interaction types
        interaction_type = webhook_data.get("type")
        
        # PING (type 1) - Discord verification
        if interaction_type == 1:
            return {
                "type": 1,  # PONG
                "status": "success"
            }
        
        # APPLICATION_COMMAND (type 2) - Slash command
        if interaction_type == 2:
            command_data = webhook_data.get("data", {})
            command_name = command_data.get("name")
            
            # Process command with AI
            if self.ai_system and command_name:
                logger.info(f"Discord: Processing command {command_name}")
                return {
                    "type": 4,  # CHANNEL_MESSAGE_WITH_SOURCE
                    "data": {
                        "content": "Processing your request with AI..."
                    },
                    "status": "success",
                    "note": "AI response would be generated here"
                }
        
        # MESSAGE_COMPONENT (type 3) - Button/select interaction
        if interaction_type == 3:
            component_data = webhook_data.get("data", {})
            custom_id = component_data.get("custom_id")
            
            logger.info(f"Discord: Processing component interaction {custom_id}")
            return {
                "type": 4,
                "data": {
                    "content": "Interaction processed"
                },
                "status": "success"
            }
        
        return {
            "status": "success",
            "interaction_type": interaction_type,
            "processed": False,
            "note": f"Interaction type {interaction_type} not handled"
        }
    
    def get_api_info(self) -> Dict[str, Any]:
        """
        Get Discord API integration information.
        
        Returns:
            Dictionary with API endpoints and documentation
        """
        return {
            "plugin": "DiscordPlugin",
            "endpoints": {
                "send_message": "/integrations/discord/send",
                "webhook": "/integrations/discord/webhook"
            },
            "required_permissions": [
                "Send Messages",
                "Read Message History",
                "Embed Links",
                "Use Slash Commands"
            ],
            "documentation": "https://discord.com/developers/docs"
        }