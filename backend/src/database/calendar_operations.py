"""
Database operations for calendar integrations
"""

from typing import Optional, Dict, Any, List
from src.database.supabase_client import db_manager
import logging

logger = logging.getLogger(__name__)

class CalendarDatabaseManager:
    """Handle calendar integration database operations"""

    async def store_calendar_integration(self,
                                       user_id: str,
                                       access_token: str,
                                       refresh_token: Optional[str],
                                       expires_at: str,
                                       scopes: List[str]) -> Optional[Dict[str, Any]]:
        """Store encrypted calendar integration data"""
        from src.services.google_calendar_service import google_calendar_service

        # Handle missing refresh token (happens on subsequent OAuth flows)
        if not access_token:
            logger.error("❌ Cannot store integration without access token")
            return None
        
        # Encrypt tokens - handle None refresh token
        encrypted_access_token = google_calendar_service.encrypt_token(access_token)
        encrypted_refresh_token = None
        if refresh_token:
            encrypted_refresh_token = google_calendar_service.encrypt_token(refresh_token)
        else:
            logger.warning("⚠️  No refresh token provided - using existing one if available")

        integration_data = {
            'user_id': user_id,
            'provider': 'google',
            'access_token': encrypted_access_token,
            'token_expires_at': expires_at,
            'scope': ' '.join(scopes) if scopes else '',
            'is_active': True
        }
        
        # Only include refresh_token if we have one
        if encrypted_refresh_token:
            integration_data['refresh_token'] = encrypted_refresh_token

        try:
            # Use upsert with the correct conflict resolution
            result = db_manager.admin.table('user_calendar_integrations').upsert(
                integration_data,
                on_conflict='user_id,provider',
                count='exact'
            ).execute()

            if result.data:
                logger.info(f"Calendar integration stored for user: {user_id}")
                return result.data[0]
            return None

        except Exception as e:
            logger.error(f"Error storing calendar integration: {e}")
            # Fallback: try to update existing record or insert new one
            try:
                # First try to update existing record
                existing = db_manager.admin.table('user_calendar_integrations').select("id").eq(
                    'user_id', user_id
                ).eq('provider', 'google').execute()
                
                if existing.data:
                    # Update existing record - don't overwrite refresh_token if we don't have a new one
                    update_data = integration_data.copy()
                    if 'refresh_token' not in update_data:
                        # Keep existing refresh_token
                        logger.info("Keeping existing refresh token")
                    
                    result = db_manager.admin.table('user_calendar_integrations').update(
                        update_data
                    ).eq('user_id', user_id).eq('provider', 'google').execute()
                    logger.info(f"Calendar integration updated for user: {user_id}")
                else:
                    # Insert new record
                    result = db_manager.admin.table('user_calendar_integrations').insert(
                        integration_data
                    ).execute()
                    logger.info(f"Calendar integration inserted for user: {user_id}")
                
                return result.data[0] if result.data else None
                
            except Exception as fallback_error:
                logger.error(f"Fallback also failed: {fallback_error}")
                return None

    async def get_user_calendar_integration(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user's calendar integration with decrypted tokens"""
        try:
            logger.info(f"📅 Fetching calendar integration for user: {user_id}")
            
            result = db_manager.admin.table('user_calendar_integrations').select("*").eq(
                'user_id', user_id
            ).eq('provider', 'google').eq('is_active', True).execute()

            print(f"🔍 Result: {result}")

            logger.info(f"📅 Database query result: {len(result.data) if result.data else 0} records found")

            if result.data:
                integration = result.data[0]
                logger.info(f"📅 Found integration record: {integration.get('id')}")
                
                # Tokens are stored directly (no decryption needed)
                logger.info("📅 Retrieved calendar integration with plain text tokens")
                
                # Validate tokens exist
                if not integration.get('access_token'):
                    logger.warning("📅 No access token found in integration")
                    return None
                    
                if not integration.get('refresh_token'):
                    logger.warning("📅 No refresh token found in integration")
                    integration['refresh_token'] = None
                
                logger.info("📅 Successfully retrieved access token")
                if integration.get('refresh_token'):
                    logger.info("📅 Successfully retrieved refresh token")
                    
                return integration
            else:
                logger.info(f"📅 No calendar integration found for user: {user_id}")
                return None

        except Exception as e:
            logger.error(f"📅 Error fetching calendar integration: {e}")
            import traceback
            logger.error(f"📅 Full traceback: {traceback.format_exc()}")
            return None

    async def log_calendar_event(self,
                                user_id: str,
                                integration_id: str,
                                event_data: Dict[str, Any],
                                original_prompt: str) -> bool:
        """Log created calendar event"""
        try:
            log_data = {
                'user_id': user_id,
                'integration_id': integration_id,
                'event_id': event_data.get('event_id'),
                'event_title': event_data.get('summary'),
                'event_description': event_data.get('description'),
                'start_time': event_data.get('start', {}).get('dateTime'),
                'end_time': event_data.get('end', {}).get('dateTime'),
                'created_via_prompt': original_prompt
            }

            db_manager.admin.table('calendar_events_log').insert(log_data).execute()
            return True

        except Exception as e:
            logger.error(f"Error logging calendar event: {e}")
            return False

# Global instance
calendar_db = CalendarDatabaseManager() 