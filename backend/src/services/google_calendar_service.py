"""
Google Calendar service for OAuth2 and calendar operations
"""

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from cryptography.fernet import Fernet
import logging

logger = logging.getLogger(__name__)

class GoogleCalendarService:
    """Handle Google Calendar OAuth2 and API operations"""

    def __init__(self):
        self.client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        self.redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/calendar/callback")
        
        # Set proper default scopes if environment variable is not set
        scopes_env = os.getenv("GOOGLE_CALENDAR_SCOPES", "")
        if scopes_env.strip():
            self.scopes = [scope.strip() for scope in scopes_env.split() if scope.strip()]
        else:
            # Default scopes for calendar access
            self.scopes = [
                "https://www.googleapis.com/auth/calendar.events",
                "https://www.googleapis.com/auth/calendar.readonly"
            ]
        
        encryption_key = os.getenv("CALENDAR_TOKEN_ENCRYPTION_KEY")
        if encryption_key:
            self.cipher = Fernet(encryption_key.encode())
        else:
            # Generate a key for development - NEVER do this in production!
            key = Fernet.generate_key()
            self.cipher = Fernet(key)
            print("⚠️  Using generated encryption key for development. Set CALENDAR_TOKEN_ENCRYPTION_KEY in production!")
        
        # Debug logging for OAuth setup
        print(f"📅 Calendar OAuth Config:")
        print(f"   Client ID: {'✅ Set' if self.client_id else '❌ Missing'}")
        print(f"   Client Secret: {'✅ Set' if self.client_secret else '❌ Missing'}")
        print(f"   Redirect URI: {self.redirect_uri}")
        print(f"   Scopes: {self.scopes}")

    def get_auth_url(self, user_id: str) -> str:
        """Get Google OAuth2 authorization URL"""
        
        # Validate OAuth credentials
        if not self.client_id or not self.client_secret:
            raise ValueError(
                "❌ Google OAuth2 credentials not configured. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables."
            )
        
        if not self.scopes:
            raise ValueError("❌ No OAuth scopes configured for Google Calendar access.")
        
        print(f"🔐 Creating OAuth URL with scopes: {self.scopes}")
        
        flow = Flow.from_client_config(
            client_config={
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uris": [self.redirect_uri],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            },
            scopes=self.scopes
        )
        flow.redirect_uri = self.redirect_uri

        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            state=user_id  # Pass user_id as state parameter
        )
        
        print(f"✅ Generated OAuth URL: {auth_url[:100]}...")
        return auth_url

    def exchange_code_for_tokens(self, code: str, user_id: str) -> Dict[str, Any]:
        """Exchange authorization code for access/refresh tokens"""
        flow = Flow.from_client_config(
            client_config={
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uris": [self.redirect_uri],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
            },
            scopes=self.scopes
        )
        flow.redirect_uri = self.redirect_uri
        flow.fetch_token(code=code)

        credentials = flow.credentials
        
        # Debug logging
        print(f"🔑 OAuth tokens received:")
        print(f"   Access token: {'✅ Present' if credentials.token else '❌ Missing'}")
        print(f"   Refresh token: {'✅ Present' if credentials.refresh_token else '❌ Missing'}")
        print(f"   Expires at: {credentials.expiry}")
        print(f"   Scopes: {credentials.scopes}")
        
        # Handle missing tokens
        if not credentials.token:
            raise ValueError("❌ No access token received from Google OAuth")
        
        return {
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,  # Can be None
            "expires_at": credentials.expiry,
            "scopes": credentials.scopes or []
        }

    def encrypt_token(self, token: str) -> str:
        """Store token directly (no encryption for development)"""
        if token is None:
            raise ValueError("❌ Cannot store None token")
        if not isinstance(token, str):
            raise ValueError(f"❌ Token must be a string, got {type(token)}")
        return token  # Return token as-is

    def decrypt_token(self, stored_token: str) -> str:
        """Retrieve token directly (no decryption needed)"""
        if stored_token is None:
            raise ValueError("❌ Cannot retrieve None token")
        if not isinstance(stored_token, str):
            raise ValueError(f"❌ Token must be a string, got {type(stored_token)}")
        return stored_token  # Return token as-is

    async def create_calendar_event(self,
                                  access_token: str,
                                  refresh_token: Optional[str],
                                  event_title: str,
                                  event_description: str = "",
                                  start_time: str = "",
                                  end_time: str = "") -> Dict[str, Any]:
        """Create a calendar event using Google Calendar API"""
        try:
            logger.info(f"📅 Creating calendar event: {event_title}")
            logger.info(f"📅 Has refresh_token: {'✅' if refresh_token else '❌'}")
            
            # Create credentials with ALL required fields for token refresh
            creds = Credentials(
                token=access_token,
                refresh_token=refresh_token,
                token_uri="https://oauth2.googleapis.com/token",  # Required for refresh
                client_id=self.client_id,
                client_secret=self.client_secret,
                scopes=self.scopes
            )

            logger.info(f"📅 Credentials created - Valid: {creds.valid}, Expired: {creds.expired}")

            # Refresh token if needed and possible
            if creds.expired and refresh_token:
                logger.info("📅 Credentials expired, attempting refresh...")
                try:
                    creds.refresh(Request())
                    logger.info("📅 Successfully refreshed credentials")
                except Exception as refresh_error:
                    logger.error(f"📅 Failed to refresh credentials: {refresh_error}")
                    return {
                        'success': False,
                        'error': f"Failed to refresh access token: {refresh_error}",
                        'message': f"❌ Failed to refresh access token: {refresh_error}"
                    }
            elif creds.expired and not refresh_token:
                logger.error("📅 Credentials expired but no refresh token available")
                return {
                    'success': False,
                    'error': "Access token expired and no refresh token available",
                    'message': "❌ Access token expired. Please reconnect your Google Calendar."
                }

            # Build Calendar API service
            logger.info("📅 Building Calendar API service...")
            service = build('calendar', 'v3', credentials=creds)

            # Create the event object with proper timezone
            event = {
                'summary': event_title,
                'description': event_description,
                'start': {
                    'dateTime': start_time,
                    'timeZone': 'Asia/Kolkata',  # Use user's timezone (IST)
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': 'Asia/Kolkata',  # Use user's timezone (IST)
                }
            }

            logger.info(f"📅 Inserting event into calendar...")
            # Insert the event
            created_event = service.events().insert(calendarId='primary', body=event).execute()
            logger.info(f"📅 Event created successfully: {created_event.get('id')}")

            return {
                'success': True,
                'event_id': created_event.get('id'),
                'event_link': created_event.get('htmlLink'),
                'message': f"✅ Calendar event '{event_title}' created successfully!"
            }

        except Exception as e:
            logger.error(f"📅 Failed to create calendar event: {e}")
            import traceback
            logger.error(f"📅 Full traceback: {traceback.format_exc()}")
            return {
                'success': False,
                'error': str(e),
                'message': f"❌ Failed to create calendar event: {e}"
            }

    async def update_stored_tokens_if_refreshed(self, user_id: str, credentials: Credentials):
        """Update stored tokens if they were refreshed"""
        try:
            from src.database.calendar_operations import calendar_db
            
            # Check if tokens were refreshed (new access_token)
            if credentials.token:
                logger.info(f"📅 Updating stored tokens for user: {user_id}")
                
                # Get current integration
                current_integration = await calendar_db.get_user_calendar_integration(user_id)
                if current_integration and current_integration.get('access_token') != credentials.token:
                    logger.info("📅 Access token was refreshed, updating database...")
                    
                    # Update with new tokens
                    await calendar_db.store_calendar_integration(
                        user_id=user_id,
                        access_token=credentials.token,
                        refresh_token=credentials.refresh_token or current_integration.get('refresh_token'),
                        expires_at=credentials.expiry.isoformat() if credentials.expiry else None,
                        scopes=credentials.scopes or []
                    )
                    logger.info("📅 Successfully updated stored tokens")
                    
        except Exception as e:
            logger.error(f"📅 Failed to update stored tokens: {e}")

    def parse_natural_language_event(self, prompt: str, user_timezone: str = 'Asia/Kolkata') -> Dict[str, Any]:
        """Parse natural language prompt into event details"""
        # This is a simplified parser - in production, use more sophisticated NLP
        import re
        from datetime import datetime, timedelta

        # Extract basic patterns (this can be enhanced with better NLP)
        title_match = re.search(r'(schedule|create|add|plan)\s+(.*?)\s+(for|at|on|tomorrow|today)', prompt, re.IGNORECASE)
        title = title_match.group(2) if title_match else "Meeting"

        # Enhanced time parsing with proper AM/PM handling
        hour = 10  # Default hour
        minute = 0  # Default minute
        
        # Look for time patterns like "10am", "2:30pm", "10:00 AM"
        time_match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)', prompt, re.IGNORECASE)
        if time_match:
            parsed_hour = int(time_match.group(1))
            parsed_minute = int(time_match.group(2)) if time_match.group(2) else 0
            am_pm = time_match.group(3).lower()
            
            # Convert to 24-hour format
            if am_pm == 'pm' and parsed_hour != 12:
                parsed_hour += 12
            elif am_pm == 'am' and parsed_hour == 12:
                parsed_hour = 0
                
            hour = parsed_hour
            minute = parsed_minute
            
            logger.info(f"📅 Parsed time: {hour:02d}:{minute:02d} from '{time_match.group(0)}'")
        else:
            logger.info(f"📅 Using default time: {hour:02d}:{minute:02d}")

        # Determine date - use timezone-aware datetime
        from datetime import timezone
        import pytz
        
        # Get user's timezone (default to India Standard Time)
        try:
            user_tz = pytz.timezone(user_timezone)
            logger.info(f"📅 Using timezone: {user_timezone}")
        except:
            # Fallback to India Standard Time if invalid timezone
            user_tz = pytz.timezone('Asia/Kolkata')
            logger.info(f"📅 Fallback to Asia/Kolkata timezone")
        
        # Get current time in user's timezone
        now_in_tz = datetime.now(user_tz)
        
        if 'tomorrow' in prompt.lower():
            event_date = now_in_tz + timedelta(days=1)
        elif 'today' in prompt.lower():
            event_date = now_in_tz
        else:
            event_date = now_in_tz + timedelta(days=1)  # Default to tomorrow

        # Set specific time in user's timezone
        start_time = event_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)  # Default 1-hour duration

        logger.info(f"📅 Event time in {user_timezone}: {start_time}")
        logger.info(f"📅 Event start: {start_time.isoformat()}")
        logger.info(f"📅 Event end: {end_time.isoformat()}")

        return {
            'title': title.title(),
            'description': f'Event created via AI assistant from: "{prompt}"',
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat()
        }

# Global instance
google_calendar_service = GoogleCalendarService() 