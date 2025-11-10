"""
Resource and Content Management for Savrli AI.

This module provides utilities for managing conversation data, sessions,
and other resources in the Savrli AI system. Supports import/export,
bulk operations, and data transformations.
"""

import json
import csv
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
from io import StringIO
import logging

logger = logging.getLogger(__name__)


class ConversationExporter:
    """Export conversation data in various formats."""
    
    @staticmethod
    def to_json(conversation_data: List[Dict[str, Any]], pretty: bool = True) -> str:
        """
        Export conversation history to JSON format.
        
        Args:
            conversation_data: List of conversation messages
            pretty: Whether to format JSON with indentation
            
        Returns:
            JSON string representation of the conversation
        """
        indent = 2 if pretty else None
        return json.dumps(conversation_data, indent=indent, default=str)
    
    @staticmethod
    def to_csv(conversation_data: List[Dict[str, Any]]) -> str:
        """
        Export conversation history to CSV format.
        
        Args:
            conversation_data: List of conversation messages
            
        Returns:
            CSV string representation of the conversation
        """
        if not conversation_data:
            return "role,content,timestamp\n"
        
        output = StringIO()
        fieldnames = ['role', 'content', 'timestamp']
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(conversation_data)
        return output.getvalue()
    
    @staticmethod
    def to_markdown(conversation_data: List[Dict[str, Any]], session_id: str) -> str:
        """
        Export conversation history to Markdown format.
        
        Args:
            conversation_data: List of conversation messages
            session_id: Session identifier
            
        Returns:
            Markdown string representation of the conversation
        """
        lines = [
            f"# Conversation History: {session_id}",
            f"",
            f"**Exported:** {datetime.now(timezone.utc).isoformat()}",
            f"**Total Messages:** {len(conversation_data)}",
            f"",
            "---",
            ""
        ]
        
        for msg in conversation_data:
            role = msg.get('role', 'unknown').upper()
            content = msg.get('content', '')
            timestamp = msg.get('timestamp', 'N/A')
            
            lines.append(f"### {role}")
            if timestamp != 'N/A':
                lines.append(f"*{timestamp}*")
            lines.append("")
            lines.append(content)
            lines.append("")
            lines.append("---")
            lines.append("")
        
        return "\n".join(lines)


class ConversationImporter:
    """Import conversation data from various formats."""
    
    @staticmethod
    def from_json(json_data: str) -> List[Dict[str, Any]]:
        """
        Import conversation history from JSON format.
        
        Args:
            json_data: JSON string containing conversation data
            
        Returns:
            List of conversation messages
            
        Raises:
            ValueError: If JSON is invalid or doesn't contain expected structure
        """
        try:
            data = json.loads(json_data)
            if not isinstance(data, list):
                raise ValueError("JSON data must be a list of messages")
            
            # Validate each message has required fields
            for msg in data:
                if not isinstance(msg, dict):
                    raise ValueError("Each message must be a dictionary")
                if 'role' not in msg or 'content' not in msg:
                    raise ValueError("Each message must have 'role' and 'content' fields")
            
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
    
    @staticmethod
    def from_csv(csv_data: str) -> List[Dict[str, Any]]:
        """
        Import conversation history from CSV format.
        
        Args:
            csv_data: CSV string containing conversation data
            
        Returns:
            List of conversation messages
            
        Raises:
            ValueError: If CSV is invalid or doesn't contain expected structure
        """
        try:
            input_stream = StringIO(csv_data)
            reader = csv.DictReader(input_stream)
            
            messages = []
            for row in reader:
                if 'role' not in row or 'content' not in row:
                    raise ValueError("CSV must have 'role' and 'content' columns")
                
                msg = {
                    'role': row['role'],
                    'content': row['content']
                }
                if 'timestamp' in row and row['timestamp']:
                    msg['timestamp'] = row['timestamp']
                
                messages.append(msg)
            
            return messages
        except Exception as e:
            raise ValueError(f"Invalid CSV: {e}")


class SessionManager:
    """Manage conversation sessions and bulk operations."""
    
    def __init__(self, conversation_history: Dict[str, List[Dict]]):
        """
        Initialize session manager.
        
        Args:
            conversation_history: Reference to the conversation history storage
        """
        self.conversation_history = conversation_history
    
    def list_sessions(
        self,
        min_messages: Optional[int] = None,
        max_messages: Optional[int] = None,
        since: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List all active sessions with optional filtering.
        
        Args:
            min_messages: Minimum number of messages
            max_messages: Maximum number of messages
            since: ISO timestamp - only sessions with messages since this time
            
        Returns:
            List of session information dictionaries
        """
        sessions = []
        
        for session_id, messages in self.conversation_history.items():
            message_count = len(messages)
            
            # Apply filters
            if min_messages is not None and message_count < min_messages:
                continue
            if max_messages is not None and message_count > max_messages:
                continue
            
            if since and messages:
                # Check if any message is after the 'since' timestamp
                has_recent = any(
                    msg.get('timestamp', '') >= since
                    for msg in messages
                )
                if not has_recent:
                    continue
            
            # Get session metadata
            first_msg = messages[0] if messages else {}
            last_msg = messages[-1] if messages else {}
            
            session_info = {
                'session_id': session_id,
                'message_count': message_count,
                'first_message_time': first_msg.get('timestamp'),
                'last_message_time': last_msg.get('timestamp'),
                'preview': last_msg.get('content', '')[:100] if last_msg else None
            }
            sessions.append(session_info)
        
        return sessions
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a specific session.
        
        Args:
            session_id: Session identifier to delete
            
        Returns:
            True if session was deleted, False if it didn't exist
        """
        if session_id in self.conversation_history:
            del self.conversation_history[session_id]
            logger.info(f"Deleted session: {session_id}")
            return True
        return False
    
    def delete_multiple_sessions(self, session_ids: List[str]) -> Dict[str, Any]:
        """
        Delete multiple sessions in bulk.
        
        Args:
            session_ids: List of session identifiers to delete
            
        Returns:
            Dictionary with deletion results
        """
        deleted = []
        not_found = []
        
        for session_id in session_ids:
            if self.delete_session(session_id):
                deleted.append(session_id)
            else:
                not_found.append(session_id)
        
        return {
            'deleted': deleted,
            'deleted_count': len(deleted),
            'not_found': not_found,
            'not_found_count': len(not_found)
        }
    
    def clear_all_sessions(self) -> int:
        """
        Clear all conversation sessions.
        
        Returns:
            Number of sessions cleared
        """
        count = len(self.conversation_history)
        self.conversation_history.clear()
        logger.warning(f"Cleared all {count} sessions")
        return count
    
    def get_session_stats(self) -> Dict[str, Any]:
        """
        Get statistics about all sessions.
        
        Returns:
            Dictionary containing session statistics
        """
        if not self.conversation_history:
            return {
                'total_sessions': 0,
                'total_messages': 0,
                'average_messages_per_session': 0,
                'largest_session': None,
                'smallest_session': None
            }
        
        message_counts = [len(msgs) for msgs in self.conversation_history.values()]
        total_messages = sum(message_counts)
        
        # Find sessions with max/min messages
        max_count = max(message_counts)
        min_count = min(message_counts)
        
        largest_session = None
        smallest_session = None
        
        for session_id, messages in self.conversation_history.items():
            if len(messages) == max_count and largest_session is None:
                largest_session = session_id
            if len(messages) == min_count and smallest_session is None:
                smallest_session = session_id
        
        return {
            'total_sessions': len(self.conversation_history),
            'total_messages': total_messages,
            'average_messages_per_session': total_messages / len(self.conversation_history),
            'largest_session': {
                'session_id': largest_session,
                'message_count': max_count
            },
            'smallest_session': {
                'session_id': smallest_session,
                'message_count': min_count
            }
        }
