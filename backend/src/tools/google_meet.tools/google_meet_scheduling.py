"""
Google Meet scheduling tool for creating meetings with Google Calendar API
"""

import os
from langchain_core.tools import tool
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timezone
import json

# Service account configuration
SERVICE_ACCOUNT_FILE = 'service-account.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Initialize and return Google Calendar service with service account authentication"""
    try:
        # Check if service account file exists
        if not os.path.exists(SERVICE_ACCOUNT_FILE):
            raise FileNotFoundError(f"Service account file '{SERVICE_ACCOUNT_FILE}' not found in project root")
        
        # Create credentials from service account file
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        
        # Build and return the service
        service = build('calendar', 'v3', credentials=credentials)
        return service
        
    except Exception as e:
        raise Exception(f"Failed to initialize Google Calendar service: {str(e)}")

def check_calendar_conference_support(service, calendar_id='primary'):
    """Check what conference types are supported by the calendar"""
    try:
        calendar = service.calendars().get(calendarId=calendar_id).execute()
        conference_properties = calendar.get('conferenceProperties', {})
        allowed_types = conference_properties.get('allowedConferenceSolutionTypes', [])
        
        print(f"📅 [GOOGLE MEET TOOL] Supported conference types: {allowed_types}")
        return allowed_types
        
    except Exception as e:
        print(f"📅 [GOOGLE MEET TOOL] Could not check conference support: {e}")
        return []

@tool
def schedule_google_meet(
    meeting_title: str, 
    description: str, 
    start_datetime: str, 
    end_datetime: str, 
    timezone_str: str = "Asia/Kolkata",
    attendees: str = "",
    calendar_id: str = "kartik.xotiv@gmail.com"
) -> str:
    """
    Schedule a Google Meet meeting using Google Calendar API.
    
    Args:
        meeting_title: Title/subject of the meeting
        description: Meeting description/agenda
        start_datetime: ISO format datetime (e.g., "2025-07-30T10:00:00+05:30")
        end_datetime: ISO format datetime for meeting end
        timezone_str: Timezone (default: "Asia/Kolkata")
        attendees: Comma-separated email addresses of attendees (optional, e.g., "john@example.com, jane@example.com")
        calendar_id: Calendar to create event in (default: "primary" = service account's calendar, or use email like "user@gmail.com")
    
    Returns:
        Meeting creation confirmation with Google Meet link and details
    """
    print(f"📅 [GOOGLE MEET TOOL] Scheduling meeting: {meeting_title}")
    
    try:
        # Initialize Google Calendar service
        service = get_calendar_service()
        
        # Check what conference types are supported for the specified calendar
        supported_types = check_calendar_conference_support(service, calendar_id)
        
        # Log which calendar we're using
        if calendar_id == "primary":
            print(f"📅 [GOOGLE MEET TOOL] Creating event in SERVICE ACCOUNT's calendar")
        else:
            print(f"📅 [GOOGLE MEET TOOL] Creating event in calendar: {calendar_id}")
        
        # Prepare attendees list if provided
        attendee_list = []
        if attendees and attendees.strip():
            # Parse comma-separated email addresses
            email_list = [email.strip() for email in attendees.split(",") if email.strip()]
            attendee_list = [{"email": email} for email in email_list]
        
        # Create basic event object
        event = {
            'summary': meeting_title,
            'description': description,
            'start': {
                'dateTime': start_datetime,
                'timeZone': timezone_str,
            },
            'end': {
                'dateTime': end_datetime,
                'timeZone': timezone_str,
            },
            'attendees': attendee_list,
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                    {'method': 'popup', 'minutes': 10},       # 10 minutes before
                ],
            },
        }
        
        # Try to create event with Google Meet first
        created_event = None
        meet_link = None
        
        try:
            # Only try Google Meet if supported
            if 'hangoutsMeet' in supported_types:
                print("📅 [GOOGLE MEET TOOL] Google Meet is supported, creating with conference data...")
                # Add Google Meet conference data - simplified structure per Google documentation
                event['conferenceData'] = {
                    'createRequest': {
                        'requestId': f"googlemeet-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    }
                }
                
                # Create the event with conferenceDataVersion=1 to enable Google Meet
                created_event = service.events().insert(
                    calendarId=calendar_id, 
                    body=event, 
                    conferenceDataVersion=1
                ).execute()
                
            else:
                print(f"📅 [GOOGLE MEET TOOL] Google Meet not supported. Available types: {supported_types}")
                print("📅 [GOOGLE MEET TOOL] Creating regular calendar event...")
                
                # Create regular event without conference data
                created_event = service.events().insert(
                    calendarId=calendar_id, 
                    body=event
                ).execute()
            
        except Exception as meet_error:
            print(f"📅 [GOOGLE MEET TOOL] Conference creation failed: {meet_error}")
            print("📅 [GOOGLE MEET TOOL] Falling back to regular calendar event...")
            
            # Remove conference data and create regular event
            if 'conferenceData' in event:
                del event['conferenceData']
            
            created_event = service.events().insert(
                calendarId=calendar_id, 
                body=event
            ).execute()
        
        # Extract meeting details
        event_id = created_event.get('id')
        html_link = created_event.get('htmlLink')
        
        # Extract Google Meet link from conference data
        if 'conferenceData' in created_event:
            conference_data = created_event['conferenceData']
            if 'entryPoints' in conference_data:
                for entry_point in conference_data['entryPoints']:
                    if entry_point.get('entryPointType') == 'video':
                        meet_link = entry_point.get('uri')
                        break
        
        # Format response
        calendar_info = "SERVICE ACCOUNT's calendar" if calendar_id == "primary" else f"calendar: {calendar_id}"
        response_parts = [
            f"✅ Meeting '{meeting_title}' scheduled successfully!",
            f"📅 Event ID: {event_id}",
            f"📋 Created in: {calendar_info}",
            f"🔗 Calendar Event: {html_link}",
        ]
        
        if meet_link:
            response_parts.append(f"🎥 Google Meet Link: {meet_link}")
        elif 'conferenceData' in created_event:
            response_parts.append("⚠️ Google Meet link generation pending (check calendar event)")
        else:
            if 'hangoutsMeet' not in supported_types:
                response_parts.append(f"⚠️ Created as regular calendar event (Google Meet not supported by calendar)")
                if supported_types:
                    response_parts.append(f"📋 Available conference types: {', '.join(supported_types)}")
                else:
                    response_parts.append("📋 No conference types available for this calendar")
            else:
                response_parts.append("⚠️ Created as regular calendar event (Google Meet creation failed)")
        
        if attendees and attendees.strip():
            email_list = [email.strip() for email in attendees.split(",") if email.strip()]
            response_parts.append(f"👥 Attendees notified: {', '.join(email_list)}")
            
        response_parts.extend([
            f"🕐 Start: {start_datetime}",
            f"🕑 End: {end_datetime}",
            f"🌍 Timezone: {timezone_str}"
        ])
        
        # Add note about service account calendar behavior
        if calendar_id == "primary":
            response_parts.append("ℹ️ Note: Event created in service account's calendar, not your personal calendar")
        
        success_msg = "\n".join(response_parts)
        print(f"📅 [GOOGLE MEET TOOL] {success_msg}")
        return success_msg
        
    except FileNotFoundError as e:
        error_msg = f"❌ Service account configuration error: {str(e)}"
        print(f"📅 [GOOGLE MEET TOOL] {error_msg}")
        return error_msg
        
    except Exception as e:
        error_msg = f"❌ Failed to schedule Google Meet: {str(e)}"
        print(f"📅 [GOOGLE MEET TOOL] {error_msg}")
        return error_msg 