"""
Integration plugins for Savrli AI

This package provides a plugin-style architecture for integrating
Savrli AI with various productivity platforms.
"""

from .plugin_base import Plugin, PluginManager
from .slack_plugin import SlackPlugin
from .discord_plugin import DiscordPlugin
from .notion_plugin import NotionPlugin
from .google_docs_plugin import GoogleDocsPlugin

__all__ = [
    "Plugin",
    "PluginManager",
    "SlackPlugin",
    "DiscordPlugin",
    "NotionPlugin",
    "GoogleDocsPlugin",
]
