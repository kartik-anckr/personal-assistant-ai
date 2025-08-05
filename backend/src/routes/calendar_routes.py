"""
Calendar OAuth2 and integration routes
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status, Query
from fastapi.responses import RedirectResponse
from src.routes.auth_routes import get_current_user
from src.models.auth_models import UserResponse
from src.services.google_calendar_service import google_calendar_service
from src.database.calendar_operations import calendar_db
from src.database.supabase_client import db_manager
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/calendar", tags=["calendar"])

class UpcomingMeetingsRequest(BaseModel):
    query: str = "next 7 days"

@router.get("/connect")
async def connect_google_calendar(current_user: UserResponse = Depends(get_current_user)):
    """Initiate Google Calendar OAuth2 flow"""
    try:
        auth_url = google_calendar_service.get_auth_url(current_user.id)
        return {"auth_url": auth_url}
    except Exception as e:
        logger.error(f"Error generating auth URL: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate authentication URL"
        )

@router.get("/callback")
async def google_calendar_callback(request: Request):
    """Handle Google OAuth2 callback"""
    code = request.query_params.get("code")
    state = request.query_params.get("state")  # This is user_id
    error = request.query_params.get("error")

    if error:
        logger.error(f"OAuth error: {error}")
        return RedirectResponse(url="http://localhost:3000/chat?calendar_error=access_denied")

    if not code or not state:
        logger.error("Missing code or state in callback")
        return RedirectResponse(url="http://localhost:3000/chat?calendar_error=invalid_callback")

    try:
        # Exchange code for tokens
        logger.info(f"📅 Processing OAuth callback for user: {state}")
        tokens = google_calendar_service.exchange_code_for_tokens(code, state)

        # Validate tokens
        if not tokens.get("access_token"):
            logger.error("❌ No access token received from Google")
            return RedirectResponse(url="http://localhost:3000/chat?calendar_error=no_access_token")

        # Store integration in database
        result = await calendar_db.store_calendar_integration(
            user_id=state,
            access_token=tokens["access_token"],
            refresh_token=tokens.get("refresh_token"),  # Use .get() since it can be None
            expires_at=tokens["expires_at"].isoformat() if tokens["expires_at"] else None,
            scopes=tokens.get("scopes", [])
        )

        if result:
            logger.info(f"✅ Google Calendar connected successfully for user: {state}")
            return RedirectResponse(url="http://localhost:3000/chat?calendar_success=connected")
        else:
            logger.error(f"❌ Failed to store calendar integration for user: {state}")
            return RedirectResponse(url="http://localhost:3000/chat?calendar_error=storage_failed")

    except Exception as e:
        logger.error(f"❌ Error in OAuth callback: {e}")
        import traceback
        traceback.print_exc()
        return RedirectResponse(url="http://localhost:3000/chat?calendar_error=connection_failed")

@router.get("/status")
async def calendar_status(current_user: UserResponse = Depends(get_current_user)):
    """Check user's calendar integration status"""
    try:
        integration = await calendar_db.get_user_calendar_integration(current_user.id)

        return {
            "connected": integration is not None,
            "provider": "google" if integration else None,
            "scopes": integration.get("scope", "").split() if integration else [],
            "connected_at": integration.get("connected_at") if integration else None
        }

    except Exception as e:
        logger.error(f"Error checking calendar status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check calendar status"
        )

@router.get("/upcoming")
async def get_upcoming_meetings_endpoint(
    query: str = Query("next 7 days", description="Time range query (e.g., 'today', 'this week', 'next month')"),
    current_user: UserResponse = Depends(get_current_user)
):
    """Get upcoming meetings from user's Google Calendar"""
    try:
        # Import upcoming_meetings_tool using direct file loading
        import importlib.util
        import os
        
        upcoming_meetings_path = os.path.join(
            os.path.dirname(__file__), '..', 'tools', 'calendar.tools', 'upcoming_meetings_tool.py'
        )
        if os.path.exists(upcoming_meetings_path):
            spec = importlib.util.spec_from_file_location("upcoming_meetings_tool", upcoming_meetings_path)
            upcoming_meetings_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(upcoming_meetings_module)
            upcoming_meetings_tool = upcoming_meetings_module.upcoming_meetings_tool
        else:
            raise Exception("Upcoming meetings tool not found")
            
        result = await upcoming_meetings_tool.get_upcoming_meetings(current_user.id, query)
        return {"meetings": result, "query": query}
    except Exception as e:
        logger.error(f"Error fetching upcoming meetings: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch upcoming meetings: {str(e)}")

@router.post("/upcoming")
async def get_upcoming_meetings_post(
    request: UpcomingMeetingsRequest,
    current_user: UserResponse = Depends(get_current_user)
):
    """Get upcoming meetings with POST request (for complex queries)"""
    try:
        # Import upcoming_meetings_tool using direct file loading
        import importlib.util
        import os
        
        upcoming_meetings_path = os.path.join(
            os.path.dirname(__file__), '..', 'tools', 'calendar.tools', 'upcoming_meetings_tool.py'
        )
        if os.path.exists(upcoming_meetings_path):
            spec = importlib.util.spec_from_file_location("upcoming_meetings_tool", upcoming_meetings_path)
            upcoming_meetings_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(upcoming_meetings_module)
            upcoming_meetings_tool = upcoming_meetings_module.upcoming_meetings_tool
        else:
            raise Exception("Upcoming meetings tool not found")
            
        result = await upcoming_meetings_tool.get_upcoming_meetings(current_user.id, request.query)
        return {"meetings": result, "query": request.query}
    except Exception as e:
        logger.error(f"Error fetching upcoming meetings: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch upcoming meetings: {str(e)}")

@router.delete("/disconnect")
async def disconnect_calendar(current_user: UserResponse = Depends(get_current_user)):
    """Disconnect user's calendar integration"""
    try:
        # Deactivate integration
        db_manager.admin.table('user_calendar_integrations').update({
            'is_active': False
        }).eq('user_id', current_user.id).eq('provider', 'google').execute()

        return {"message": "Calendar disconnected successfully"}

    except Exception as e:
        logger.error(f"Error disconnecting calendar: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to disconnect calendar"
        ) 