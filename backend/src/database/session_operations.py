"""
Chat session database operations
"""

from typing import List, Optional, Dict, Any
from .supabase_client import db_manager
import logging

logger = logging.getLogger(__name__)

class SessionManager:
    """Manage chat session database operations"""

    async def create_session(self, user_id: str, title: str = "New Chat", description: str = None, jwt_token: str = None) -> Optional[Dict[str, Any]]:
        """Create a new chat session for user"""
        try:
            session_data = {
                "user_id": user_id,
                "title": title,
                "description": description,
                "is_active": True
            }
            
            # Use admin client if available, otherwise use regular client with user filtering
            client = db_manager.admin if db_manager.admin else db_manager.client
            if not client:
                logger.error("No database client available")
                return None
                
            result = client.table('chat_sessions').insert(session_data).execute()
            if result.data:
                logger.info(f"Created session {result.data[0]['id']} for user {user_id}")
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            return None

    async def get_user_sessions(self, user_id: str, active_only: bool = True) -> List[Dict[str, Any]]:
        """Get all sessions for a user"""
        try:
            query = db_manager.client.from_('session_stats').select("*").eq('user_id', user_id)
            if active_only:
                query = query.eq('is_active', True)
            query = query.order('last_message_at', desc=True)

            result = query.execute()
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Error fetching user sessions: {e}")
            return []

    async def get_session(self, session_id: str, user_id: str, jwt_token: str = None) -> Optional[Dict[str, Any]]:
        """Get a specific session"""
        try:
            # Use admin client if available, otherwise use regular client with user filtering
            client = db_manager.admin if db_manager.admin else db_manager.client
            if not client:
                logger.error("No database client available")
                return None
                
            result = client.table('chat_sessions').select("*").eq('id', session_id).eq('user_id', user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error fetching session: {e}")
            return None

    async def get_session_with_stats(self, session_id: str, user_id: str, jwt_token: str = None) -> Optional[Dict[str, Any]]:
        """Get a specific session with message stats from session_stats view"""
        try:
            # Use admin client if available, otherwise use regular client with user filtering
            client = db_manager.admin if db_manager.admin else db_manager.client
            if not client:
                logger.error("No database client available")
                return None
                
            result = client.from_('session_stats').select("*").eq('id', session_id).eq('user_id', user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error fetching session with stats: {e}")
            return None

    async def update_session(self, session_id: str, user_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update session information"""
        try:
            update_data['updated_at'] = 'NOW()'
            result = db_manager.client.table('chat_sessions').update(update_data).eq('id', session_id).eq('user_id', user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error updating session: {e}")
            return None

    async def delete_session(self, session_id: str, user_id: str) -> bool:
        """Delete a session (soft delete by setting inactive)"""
        try:
            result = db_manager.client.table('chat_sessions').update({
                'is_active': False,
                'updated_at': 'NOW()'
            }).eq('id', session_id).eq('user_id', user_id).execute()
            return bool(result.data)
        except Exception as e:
            logger.error(f"Error deleting session: {e}")
            return False

    async def update_session_last_message(self, session_id: str) -> bool:
        """Update session's last_message_at timestamp"""
        try:
            db_manager.client.table('chat_sessions').update({
                'last_message_at': 'NOW()',
                'updated_at': 'NOW()'
            }).eq('id', session_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error updating session timestamp: {e}")
            return False

# Global instance
session_manager = SessionManager() 