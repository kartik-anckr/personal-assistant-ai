"""
Chat session management API routes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from ..models.auth_models import UserResponse
from ..routes.auth_routes import get_current_user, get_current_user_with_token
from ..database.session_operations import session_manager
from ..database.message_operations import message_manager

router = APIRouter(prefix="/sessions", tags=["sessions"])

# Request/Response Models
class CreateSessionRequest(BaseModel):
    title: str = "New Chat"
    description: Optional[str] = None

class UpdateSessionRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class SessionResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    is_active: bool
    created_at: str
    updated_at: str
    last_message_at: str
    message_count: int
    last_message_preview: str

class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    metadata: dict
    message_order: int
    created_at: str

@router.post("/", response_model=SessionResponse)
async def create_session(
    request: CreateSessionRequest,
    user_and_token: tuple[UserResponse, str] = Depends(get_current_user_with_token)
):
    """Create a new chat session"""
    current_user, jwt_token = user_and_token
    
    session = await session_manager.create_session(
        user_id=current_user.id,
        title=request.title,
        description=request.description,
        jwt_token=jwt_token
    )

    if not session:
        raise HTTPException(status_code=500, detail="Failed to create session")

    # Get the enriched session data with message count and preview
    enriched_session = await session_manager.get_session_with_stats(session["id"], current_user.id, jwt_token)
    
    if not enriched_session:
        raise HTTPException(status_code=500, detail="Failed to retrieve created session")

    return enriched_session

@router.get("/", response_model=List[SessionResponse])
async def get_sessions(
    active_only: bool = Query(True, description="Only return active sessions"),
    user_and_token: tuple[UserResponse, str] = Depends(get_current_user_with_token)
):
    """Get all sessions for the current user"""
    current_user, jwt_token = user_and_token
    
    sessions = await session_manager.get_user_sessions(current_user.id, active_only)
    return sessions

@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    user_and_token: tuple[UserResponse, str] = Depends(get_current_user_with_token)
):
    """Get a specific session"""
    current_user, jwt_token = user_and_token
    
    session = await session_manager.get_session_with_stats(session_id, current_user.id, jwt_token)

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return session

@router.put("/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: str,
    request: UpdateSessionRequest,
    user_and_token: tuple[UserResponse, str] = Depends(get_current_user_with_token)
):
    """Update session information"""
    current_user, jwt_token = user_and_token
    
    update_data = {}
    if request.title is not None:
        update_data["title"] = request.title
    if request.description is not None:
        update_data["description"] = request.description

    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")

    updated_session = await session_manager.update_session(session_id, current_user.id, update_data)

    if not updated_session:
        raise HTTPException(status_code=404, detail="Session not found or update failed")

    # Get the enriched session data with message count and preview
    enriched_session = await session_manager.get_session_with_stats(session_id, current_user.id, jwt_token)
    
    if not enriched_session:
        raise HTTPException(status_code=500, detail="Failed to retrieve updated session")

    return enriched_session

@router.delete("/{session_id}")
async def delete_session(
    session_id: str,
    user_and_token: tuple[UserResponse, str] = Depends(get_current_user_with_token)
):
    """Delete (deactivate) a session"""
    current_user, jwt_token = user_and_token
    
    success = await session_manager.delete_session(session_id, current_user.id)

    if not success:
        raise HTTPException(status_code=404, detail="Session not found or delete failed")

    return {"message": "Session deleted successfully"}

@router.get("/{session_id}/messages", response_model=List[MessageResponse])
async def get_session_messages(
    session_id: str,
    limit: Optional[int] = Query(None, description="Maximum number of messages to return"),
    offset: int = Query(0, description="Number of messages to skip"),
    user_and_token: tuple[UserResponse, str] = Depends(get_current_user_with_token)
):
    """Get messages for a session"""
    current_user, jwt_token = user_and_token
    
    # Verify session exists and belongs to user
    session = await session_manager.get_session(session_id, current_user.id, jwt_token)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = await message_manager.get_session_messages(
        session_id, current_user.id, limit, offset, jwt_token
    )

    return messages

@router.delete("/{session_id}/messages")
async def clear_session_messages(
    session_id: str,
    user_and_token: tuple[UserResponse, str] = Depends(get_current_user_with_token)
):
    """Clear all messages in a session"""
    current_user, jwt_token = user_and_token
    
    # Verify session exists and belongs to user
    session = await session_manager.get_session(session_id, current_user.id, jwt_token)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    success = await message_manager.delete_session_messages(session_id, current_user.id)

    if not success:
        raise HTTPException(status_code=500, detail="Failed to clear messages")

    return {"message": "Session messages cleared successfully"} 