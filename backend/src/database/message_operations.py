"""
Chat message database operations
"""

from typing import List, Optional, Dict, Any
from .supabase_client import db_manager
from .session_operations import session_manager
import logging

logger = logging.getLogger(__name__)

class MessageManager:
    """Manage chat message database operations"""

    async def add_message(self, session_id: str, user_id: str, role: str, content: str, metadata: Dict[str, Any] = None, jwt_token: str = None) -> Optional[Dict[str, Any]]:
        """Add a new message to a session"""
        try:
            # Use admin client if available, otherwise use regular client with user filtering
            client = db_manager.admin if db_manager.admin else db_manager.client
            if not client:
                logger.error("No database client available")
                return None
                
            # Get next message order
            order_result = client.table('chat_messages').select("message_order").eq('session_id', session_id).order('message_order', desc=True).limit(1).execute()
            next_order = (order_result.data[0]['message_order'] + 1) if order_result.data else 1

            message_data = {
                "session_id": session_id,
                "user_id": user_id,
                "role": role,
                "content": content,
                "metadata": metadata or {},
                "message_order": next_order
            }

            result = client.table('chat_messages').insert(message_data).execute()
            if result.data:
                # Update session last message timestamp
                await session_manager.update_session_last_message(session_id)
                logger.info(f"Added message {result.data[0]['id']} to session {session_id}")
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error adding message: {e}")
            return None

    async def get_session_messages(self, session_id: str, user_id: str, limit: int = None, offset: int = 0, jwt_token: str = None) -> List[Dict[str, Any]]:
        """Get messages for a session"""
        try:
            # Use admin client if available, otherwise use regular client with user filtering
            client = db_manager.admin if db_manager.admin else db_manager.client
            if not client:
                logger.error("No database client available")
                return []
                
            query = client.table('chat_messages').select("*").eq('session_id', session_id).eq('user_id', user_id).order('message_order')

            if limit:
                query = query.limit(limit).offset(offset)

            result = query.execute()
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Error fetching session messages: {e}")
            return []

    async def get_recent_messages(self, session_id: str, user_id: str, count: int = 50) -> List[Dict[str, Any]]:
        """Get recent messages for context (optimized for LangGraph)"""
        try:
            # Use admin client if available, otherwise use regular client with user filtering
            client = db_manager.admin if db_manager.admin else db_manager.client
            if not client:
                logger.error("No database client available")
                return []
                
            result = client.table('chat_messages').select("*").eq('session_id', session_id).eq('user_id', user_id).order('message_order', desc=True).limit(count).execute()

            # Return in correct order (oldest first)
            return list(reversed(result.data)) if result.data else []
        except Exception as e:
            logger.error(f"Error fetching recent messages: {e}")
            return []

    async def delete_session_messages(self, session_id: str, user_id: str) -> bool:
        """Delete all messages in a session"""
        try:
            db_manager.client.table('chat_messages').delete().eq('session_id', session_id).eq('user_id', user_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error deleting session messages: {e}")
            return False

    async def update_message(self, message_id: str, user_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a specific message"""
        try:
            update_data['updated_at'] = 'NOW()'
            result = db_manager.client.table('chat_messages').update(update_data).eq('id', message_id).eq('user_id', user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error updating message: {e}")
            return None

# Global instance
message_manager = MessageManager() 