"""
Google Calendar tools for event creation and upcoming meetings retrieval
"""

from langchain_core.tools import tool
from src.services.google_calendar_service import google_calendar_service
from src.database.calendar_operations import calendar_db
import asyncio
import logging

# Import the upcoming meetings function using direct file loading
import sys
import os
import importlib.util

_upcoming_meetings_path = os.path.join(os.path.dirname(__file__), 'upcoming_meetings_tool.py')
if os.path.exists(_upcoming_meetings_path):
    spec = importlib.util.spec_from_file_location("upcoming_meetings_tool", _upcoming_meetings_path)
    upcoming_meetings_module = importlib.util.module_from_spec(spec)
    sys.modules['upcoming_meetings_tool'] = upcoming_meetings_module
    spec.loader.exec_module(upcoming_meetings_module)
    get_upcoming_meetings = upcoming_meetings_module.get_upcoming_meetings
else:
    # If file doesn't exist, create a dummy function
    async def get_upcoming_meetings(query: str = "next 7 days", user_id: str = None) -> str:
        return "❌ Upcoming meetings feature not available due to import error."

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

@tool
def get_upcoming_meetings_tool(query: str = "next 7 days", user_id: str = None) -> str:
    """
    Get upcoming meetings from Google Calendar.
    
    Args:
        query: Natural language query describing the time range (e.g., "today", "this week", "next month")
        user_id: ID of the user to fetch calendar for
    
    Returns:
        Formatted string with upcoming meetings
    """
    logger.info(f"📅 Getting upcoming meetings for user {user_id}: {query}")
    
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
        # Use the async function from the upcoming_meetings_tool module
        result = asyncio.run(get_upcoming_meetings(query, user_id))
        return result
    except Exception as e:
        error_msg = f"❌ Failed to get upcoming meetings: {str(e)}"
        logger.error(error_msg)
        return error_msg

def create_calendar_tools():
    """Create list of calendar tools"""
    return [create_calendar_event, get_upcoming_meetings_tool] 