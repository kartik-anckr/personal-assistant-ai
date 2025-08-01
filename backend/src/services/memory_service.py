"""
LangGraph memory service for session-based conversation history
"""

from typing import Optional, Dict, Any, List
import os
import logging

logger = logging.getLogger(__name__)

# Try to import LangGraph checkpointers, fall back to None if not available
try:
    from langgraph.checkpoint.postgres import PostgresSaver
    from langgraph.checkpoint.memory import InMemorySaver
    CHECKPOINTERS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"LangGraph checkpointers not available: {e}")
    logger.warning("Session memory will work but without LangGraph checkpoint persistence")
    PostgresSaver = None
    InMemorySaver = None
    CHECKPOINTERS_AVAILABLE = False

# Import message manager with error handling
try:
    from ..database.message_operations import message_manager
except ImportError:
    logger.error("Could not import message_manager - database operations may not work")
    message_manager = None

class MemoryService:
    """Manage LangGraph memory and checkpoints for chat sessions"""

    def __init__(self):
        self.checkpointer = None
        self._setup_checkpointer()

    def _setup_checkpointer(self):
        """Setup LangGraph checkpointer based on environment"""
        if not CHECKPOINTERS_AVAILABLE:
            logger.warning("LangGraph checkpointers not available - memory persistence disabled")
            self.checkpointer = None
            return

        database_url = os.getenv("DATABASE_URL")

        if database_url and database_url.startswith("postgresql://") and PostgresSaver:
            try:
                # Use PostgreSQL checkpointer for production
                self.checkpointer = PostgresSaver.from_conn_string(database_url)
                self.checkpointer.setup()
                logger.info("Initialized PostgreSQL checkpointer for memory")
            except Exception as e:
                logger.warning(f"Failed to setup PostgreSQL checkpointer, falling back to memory: {e}")
                if InMemorySaver:
                    self.checkpointer = InMemorySaver()
                else:
                    self.checkpointer = None
        else:
            # Use in-memory checkpointer for development
            if InMemorySaver:
                self.checkpointer = InMemorySaver()
                logger.info("Initialized in-memory checkpointer for memory")
            else:
                self.checkpointer = None
                logger.warning("No checkpointer available")

    def get_checkpointer(self):
        """Get the configured checkpointer"""
        return self.checkpointer

    async def load_session_context(self, session_id: str, user_id: str, max_messages: int = 50) -> List[Dict[str, Any]]:
        """Load recent messages from database for session context"""
        if not message_manager:
            logger.warning("Message manager not available - returning empty context")
            return []
            
        try:
            messages = await message_manager.get_recent_messages(session_id, user_id, max_messages)

            # Convert database messages to LangGraph format
            langgraph_messages = []
            for msg in messages:
                message_data = {
                    "role": msg["role"],
                    "content": msg["content"]
                }

                # Add metadata if present
                if msg.get("metadata"):
                    message_data.update(msg["metadata"])

                langgraph_messages.append(message_data)

            logger.info(f"Loaded {len(langgraph_messages)} messages for session {session_id}")
            return langgraph_messages

        except Exception as e:
            logger.error(f"Error loading session context: {e}")
            return []

    async def save_messages_to_db(self, session_id: str, user_id: str, messages: List[Dict[str, Any]]) -> bool:
        """Save new messages to database"""
        if not message_manager:
            logger.warning("Message manager not available - cannot save messages")
            return False
            
        try:
            for message in messages:
                await message_manager.add_message(
                    session_id=session_id,
                    user_id=user_id,
                    role=message.get("role", "assistant"),
                    content=str(message.get("content", "")),
                    metadata=message.get("metadata", {})
                )
            return True
        except Exception as e:
            logger.error(f"Error saving messages to database: {e}")
            return False

    def get_thread_config(self, session_id: str) -> Dict[str, Any]:
        """Get LangGraph thread configuration for a session"""
        return {
            "configurable": {
                "thread_id": session_id
            }
        }

# Global instance
memory_service = MemoryService() 