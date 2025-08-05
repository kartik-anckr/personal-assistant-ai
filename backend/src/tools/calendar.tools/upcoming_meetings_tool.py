"""
Tool for retrieving upcoming meetings from Google Calendar
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import pytz
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging
import re
import asyncio

# Import calendar_db using direct file loading
import sys
import os
import importlib.util

# Try to import calendar_db directly
calendar_db = None
try:
    # First try standard import
    from src.database.calendar_operations import calendar_db
except ImportError:
    # Try to load it directly from file
    calendar_operations_path = os.path.join(
        os.path.dirname(__file__), '..', '..', 'database', 'calendar_operations.py'
    )
    if os.path.exists(calendar_operations_path):
        spec = importlib.util.spec_from_file_location("calendar_operations", calendar_operations_path)
        calendar_operations_module = importlib.util.module_from_spec(spec)
        sys.modules['calendar_operations'] = calendar_operations_module
        spec.loader.exec_module(calendar_operations_module)
        calendar_db = calendar_operations_module.calendar_db
    else:
        # Create a dummy calendar_db if import fails
        class DummyCalendarDB:
            async def get_user_calendar_integration(self, user_id: str):
                return None
        calendar_db = DummyCalendarDB()

logger = logging.getLogger(__name__)

class UpcomingMeetingsTool:
    """Tool for fetching upcoming meetings from Google Calendar"""

    def __init__(self):
        self.service_name = 'calendar'
        self.service_version = 'v3'

    def parse_date_range(self, query: str) -> tuple[datetime, datetime]:
        """Parse natural language date range from user query"""
        now = datetime.now(pytz.UTC)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Convert query to lowercase for easier matching
        query_lower = query.lower()
        
        # Today
        if any(word in query_lower for word in ['today', 'today\'s']):
            start_time = today_start
            end_time = today_start + timedelta(days=1)
        
        # Tomorrow
        elif any(word in query_lower for word in ['tomorrow', 'tomorrow\'s']):
            start_time = today_start + timedelta(days=1)
            end_time = start_time + timedelta(days=1)
        
        # This week
        elif any(phrase in query_lower for phrase in ['this week', 'week']):
            # Start from today, end 7 days from now
            start_time = today_start
            end_time = today_start + timedelta(days=7)
        
        # Next week
        elif any(phrase in query_lower for phrase in ['next week']):
            # Start from next Monday, end following Sunday
            days_until_next_monday = (7 - now.weekday()) % 7
            if days_until_next_monday == 0:  # If today is Monday
                days_until_next_monday = 7
            start_time = today_start + timedelta(days=days_until_next_monday)
            end_time = start_time + timedelta(days=7)
        
        # This month
        elif any(phrase in query_lower for phrase in ['this month', 'month']):
            start_time = today_start
            # End of current month
            if now.month == 12:
                end_time = now.replace(year=now.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            else:
                end_time = now.replace(month=now.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Default: next 7 days
        else:
            start_time = today_start
            end_time = today_start + timedelta(days=7)
        
        return start_time, end_time

    def build_calendar_service(self, user_credentials: Dict[str, Any]):
        """Build Google Calendar service with user credentials"""
        try:
            # Create credentials object
            credentials = Credentials(
                token=user_credentials['access_token'],
                refresh_token=user_credentials.get('refresh_token'),
                token_uri="https://oauth2.googleapis.com/token",
                client_id=user_credentials.get('client_id'),
                client_secret=user_credentials.get('client_secret'),
                scopes=user_credentials.get('scope', '').split()
            )
            
            # Build and return the service
            service = build(self.service_name, self.service_version, credentials=credentials)
            return service
            
        except Exception as e:
            logger.error(f"Error building calendar service: {e}")
            raise e

    def fetch_calendar_events(
        self, 
        service, 
        start_time: datetime, 
        end_time: datetime,
        max_results: int = 50
    ) -> List[Dict[str, Any]]:
        """Fetch events from Google Calendar API"""
        try:
            # Convert to RFC3339 format
            time_min = start_time.isoformat()
            time_max = end_time.isoformat()
            
            # Call the Calendar API
            events_result = service.events().list(
                calendarId='primary',
                timeMin=time_min,
                timeMax=time_max,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            logger.info(f"Retrieved {len(events)} events from Google Calendar")
            return events
            
        except HttpError as e:
            logger.error(f"Google Calendar API error: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error fetching calendar events: {e}")
            raise e

    def format_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Format a single calendar event for display"""
        try:
            # Extract basic information
            summary = event.get('summary', 'No Title')
            description = event.get('description', '')
            location = event.get('location', '')
            
            # Handle start and end times
            start = event.get('start', {})
            end = event.get('end', {})
            
            # Handle all-day events
            if 'date' in start:
                start_time = start['date']
                end_time = end.get('date', start_time)
                is_all_day = True
            else:
                start_time = start.get('dateTime', '')
                end_time = end.get('dateTime', '')
                is_all_day = False
            
            # Format attendees
            attendees = []
            for attendee in event.get('attendees', []):
                attendee_info = {
                    'email': attendee.get('email', ''),
                    'name': attendee.get('displayName', attendee.get('email', '')),
                    'status': attendee.get('responseStatus', 'needsAction')
                }
                attendees.append(attendee_info)
            
            # Meeting link extraction
            meeting_link = ''
            if 'hangoutLink' in event:
                meeting_link = event['hangoutLink']
            elif description:
                # Look for common meeting links in description
                meeting_patterns = [
                    r'https://meet\.google\.com/[a-z-]+',
                    r'https://zoom\.us/j/\d+',
                    r'https://teams\.microsoft\.com/[^\s]+',
                    r'https://.*webex.*\.com/[^\s]+'
                ]
                for pattern in meeting_patterns:
                    match = re.search(pattern, description)
                    if match:
                        meeting_link = match.group()
                        break
            
            formatted_event = {
                'id': event.get('id', ''),
                'title': summary,
                'description': description,
                'location': location,
                'start_time': start_time,
                'end_time': end_time,
                'is_all_day': is_all_day,
                'attendees': attendees,
                'meeting_link': meeting_link,
                'calendar_link': event.get('htmlLink', ''),
                'status': event.get('status', 'confirmed'),
                'creator': event.get('creator', {}).get('displayName', ''),
                'organizer': event.get('organizer', {}).get('displayName', '')
            }
            
            return formatted_event
            
        except Exception as e:
            logger.error(f"Error formatting event: {e}")
            return {
                'title': event.get('summary', 'Error formatting event'),
                'error': str(e)
            }

    def format_events_response(self, events: List[Dict[str, Any]], date_range: str) -> str:
        """Format list of events into a user-friendly response"""
        if not events:
            return f"📅 You have no upcoming meetings {date_range}."
        
        response_lines = [f"📅 **Your upcoming meetings {date_range}:**\n"]
        
        current_date = None
        for i, event in enumerate(events, 1):
            try:
                # Group by date
                if event['is_all_day']:
                    event_date = event['start_time']
                else:
                    event_datetime = datetime.fromisoformat(event['start_time'].replace('Z', '+00:00'))
                    event_date = event_datetime.strftime('%Y-%m-%d')
                
                if event_date != current_date:
                    if current_date is not None:
                        response_lines.append("")  # Add spacing between dates
                    
                    # Format date header
                    try:
                        date_obj = datetime.fromisoformat(event_date + 'T00:00:00')
                        date_header = date_obj.strftime('%A, %B %d, %Y')
                    except:
                        date_header = event_date
                    
                    response_lines.append(f"**{date_header}:**")
                    current_date = event_date
                
                # Format individual event
                event_line = f"  {i}. **{event['title']}**"
                
                # Add time information
                if event['is_all_day']:
                    event_line += " (All day)"
                else:
                    try:
                        start_dt = datetime.fromisoformat(event['start_time'].replace('Z', '+00:00'))
                        end_dt = datetime.fromisoformat(event['end_time'].replace('Z', '+00:00'))
                        time_str = f"{start_dt.strftime('%I:%M %p')} - {end_dt.strftime('%I:%M %p')}"
                        event_line += f" ({time_str})"
                    except:
                        event_line += f" ({event['start_time']})"
                
                response_lines.append(event_line)
                
                # Add location if available
                if event.get('location'):
                    response_lines.append(f"     📍 {event['location']}")
                
                # Add meeting link if available
                if event.get('meeting_link'):
                    response_lines.append(f"     🔗 {event['meeting_link']}")
                
                # Add attendees count if applicable
                attendees = event.get('attendees', [])
                if attendees:
                    response_lines.append(f"     👥 {len(attendees)} attendee{'s' if len(attendees) > 1 else ''}")
                
                # Add description preview if available
                if event.get('description') and len(event['description']) > 0:
                    desc_preview = event['description'][:100]
                    if len(event['description']) > 100:
                        desc_preview += "..."
                    response_lines.append(f"     📝 {desc_preview}")
                
            except Exception as e:
                logger.error(f"Error formatting event {i}: {e}")
                response_lines.append(f"  {i}. {event.get('title', 'Unknown event')} (formatting error)")
        
        return "\n".join(response_lines)

    async def get_upcoming_meetings(self, user_id: str, query: str = "next 7 days") -> str:
        """Main function to get and format upcoming meetings"""
        try:
            # Get user's calendar credentials
            credentials = await self.get_user_calendar_credentials(user_id)
            if not credentials:
                return "❌ No Google Calendar connected. Please connect your Google Calendar first."
            
            # Parse date range from query
            start_time, end_time = self.parse_date_range(query)
            
            # Determine date range description for response
            now = datetime.now(pytz.UTC)
            if start_time.date() == now.date() and end_time.date() == (now + timedelta(days=1)).date():
                date_range_desc = "today"
            elif start_time.date() == (now + timedelta(days=1)).date():
                date_range_desc = "tomorrow"
            elif (end_time - start_time).days == 7:
                date_range_desc = "this week"
            else:
                date_range_desc = f"from {start_time.strftime('%b %d')} to {end_time.strftime('%b %d')}"
            
            # Build Google Calendar service
            service = self.build_calendar_service(credentials)
            
            # Fetch events
            events = self.fetch_calendar_events(service, start_time, end_time)
            
            # Format events
            formatted_events = []
            for event in events:
                formatted_event = self.format_event(event)
                formatted_events.append(formatted_event)
            
            # Generate response
            response = self.format_events_response(formatted_events, date_range_desc)
            
            logger.info(f"Successfully retrieved {len(formatted_events)} meetings for user {user_id}")
            return response
            
        except Exception as e:
            error_msg = f"Failed to retrieve upcoming meetings: {str(e)}"
            logger.error(error_msg)
            return f"❌ {error_msg}"

    async def get_user_calendar_credentials(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user's calendar credentials for API calls"""
        try:
            from src.services.google_calendar_service import google_calendar_service
            import os
            
            # Get integration from database
            integration = await calendar_db.get_user_calendar_integration(user_id)
            
            if integration:
                # Decrypt credentials
                access_token = google_calendar_service.decrypt_token(integration['access_token'])
                refresh_token = None
                if integration.get('refresh_token'):
                    refresh_token = google_calendar_service.decrypt_token(integration['refresh_token'])
                
                return {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'token_expires_at': integration.get('token_expires_at'),
                    'scope': integration.get('scope'),
                    'client_id': os.getenv('GOOGLE_CLIENT_ID'),
                    'client_secret': os.getenv('GOOGLE_CLIENT_SECRET')
                }
            return None
        except Exception as e:
            logger.error(f"Error fetching calendar credentials: {e}")
            return None

# Global instance
upcoming_meetings_tool = UpcomingMeetingsTool()

# Tool function for LangGraph integration
async def get_upcoming_meetings(query: str = "next 7 days", user_id: str = None) -> str:
    """
    LangGraph tool function to get upcoming meetings from Google Calendar
    
    Args:
        query: Natural language query describing the time range (e.g., "today", "this week", "next month")
        user_id: User ID to fetch calendar for
    
    Returns:
        Formatted string with upcoming meetings
    """
    if not user_id:
        return "❌ User ID is required to fetch calendar events."
    
    return await upcoming_meetings_tool.get_upcoming_meetings(user_id, query) 