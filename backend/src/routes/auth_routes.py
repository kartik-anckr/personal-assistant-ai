"""
Authentication API routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.models.auth_models import (
    UserSignupRequest,
    UserSigninRequest,
    AuthResponse,
    UserResponse
)
from src.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserResponse:
    """Dependency to get current authenticated user"""
    return await auth_service.get_current_user(credentials.credentials)

async def get_current_user_with_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> tuple[UserResponse, str]:
    """Dependency to get current authenticated user and JWT token"""
    user = await auth_service.get_current_user(credentials.credentials)
    return user, credentials.credentials

@router.post("/signup", response_model=AuthResponse)
async def signup(signup_data: UserSignupRequest):
    """Register a new user"""
    return await auth_service.signup_user(signup_data)

@router.post("/signin", response_model=AuthResponse)
async def signin(signin_data: UserSigninRequest):
    """Authenticate user login"""
    return await auth_service.signin_user(signin_data)

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    """Get current user profile"""
    return current_user

@router.get("/verify-token")
async def verify_token(current_user: UserResponse = Depends(get_current_user)):
    """Verify if token is valid"""
    return {"valid": True, "user_id": current_user.id} 