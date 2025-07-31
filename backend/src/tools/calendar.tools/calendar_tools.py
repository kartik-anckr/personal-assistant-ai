"""
Google Calendar tools for event creation
"""

from langchain_core.tools import tool
from src.services.google_calendar_service import google_calendar_service
from src.database.calendar_operations import calendar_db
import asyncio
import logging

logger = logging.getLogger(__name__)

@tool
def create_calendar_event(prompt: str, user_id: str) -> str:
    """
    Create a calendar event from natural language prompt.

    Args:
        prompt: Natural language description of the event (e.g., "Schedule meeting tomorrow at 2pm")
        user_id: ID of the user creating the event

    Returns:
        Success message with event details or error message
    """
    logger.info(f"📅 Creating calendar event for user {user_id}: {prompt}")
    
    # Validate user_id format
    if not user_id or user_id in ["unknown", "user123", ""]:
        return "❌ Invalid user session. Please ensure you're properly logged in to use calendar features."
    
    # Basic UUID format validation
    import re
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
    if not re.match(uuid_pattern, user_id, re.IGNORECASE):
        logger.error(f"❌ Invalid UUID format for user_id: {user_id}")
        return "❌ Invalid user ID format. Please log in again to use calendar features."

    try:
        # Check if user has calendar integration
        logger.info(f"📅 Checking calendar integration for user: {user_id}")
        integration = asyncio.run(calendar_db.get_user_calendar_integration(user_id))
        print(f"🔍 Integration: {integration}")
        if not integration:
            return "❌ Please connect your Google Calendar first. Go to chat settings to connect your calendar."

        # Parse natural language into event details
        event_details = google_calendar_service.parse_natural_language_event(prompt)

        # Create the event using Google Calendar API
        result = asyncio.run(google_calendar_service.create_calendar_event(
            access_token=integration['access_token'],
            refresh_token=integration.get('refresh_token'),
            event_title=event_details['title'],
            event_description=event_details['description'],
            start_time=event_details['start_time'],
            end_time=event_details['end_time']
        ))

        # Log the created event if successful
        if result.get('success'):
            asyncio.run(calendar_db.log_calendar_event(
                user_id=user_id,
                integration_id=integration['id'],
                event_data={
                    'title': event_details['title'],
                    'description': event_details['description'],
                    'start_time': event_details['start_time'],
                    'end_time': event_details['end_time'],
                    'event_id': result.get('event_id', '')
                },
                original_prompt=prompt
            ))
            
        return result.get('message', 'Calendar event created successfully!')  if result.get('success') else result.get('message', 'Failed to create calendar event')



    except Exception as e:
        error_msg = f"❌ Failed to create calendar event: {str(e)}"
        logger.error(error_msg)
        return error_msg

def create_calendar_tools():
    """Create list of calendar tools"""
    return [create_calendar_event] 