"""
Authentication service with JWT token management
"""

import os
import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from src.database.supabase_client import db_manager
from src.models.auth_models import UserSignupRequest, UserSigninRequest, UserResponse, AuthResponse

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

class AuthService:
    """Handle authentication operations"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def create_access_token(data: Dict[str, Any]) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.PyJWTError:
            return None

    async def signup_user(self, signup_data: UserSignupRequest) -> AuthResponse:
        """Register new user"""

        # Check if user already exists
        existing_user = await db_manager.get_user_by_email(signup_data.email)
        if existing_user is None:
            # If None is returned, it could mean database is unavailable or user doesn't exist
            # We can't distinguish, so for now we'll continue with user creation
            pass
        elif existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        # Check if username already exists
        existing_username = await db_manager.get_user_by_username(signup_data.username)
        if existing_username is None:
            # If None is returned, it could mean database is unavailable or user doesn't exist
            # We can't distinguish, so for now we'll continue with user creation
            pass
        elif existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username is already taken"
            )

        # Hash password
        hashed_password = self.hash_password(signup_data.password)

        # Prepare user data
        user_data = {
            "username": signup_data.username,
            "email": signup_data.email,
            "password_hash": hashed_password,
            "first_name": signup_data.first_name,
            "last_name": signup_data.last_name,
            "is_active": True
        }

        # Create user in database
        created_user = await db_manager.create_user(user_data)
        print(f"Created user: {created_user}")
        if not created_user:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database service unavailable. Please configure Supabase environment variables."
            )

        # Generate access token
        token_data = {"user_id": created_user["id"], "email": created_user["email"]}
        access_token = self.create_access_token(token_data)

        # Prepare response
        user_response = UserResponse(**created_user)
        return AuthResponse(
            user=user_response,
            access_token=access_token,
            expires_in=JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

    async def signin_user(self, signin_data: UserSigninRequest) -> AuthResponse:
        """Authenticate user login"""

        # Get user from database using admin client (to bypass RLS)
        user = await db_manager.get_user_by_email_admin(signin_data.email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Verify password
        if not self.verify_password(signin_data.password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Check if user is active
        if not user["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated"
            )

        # Update last login
        await db_manager.update_last_login(user["id"])

        # Generate access token
        token_data = {"user_id": user["id"], "email": user["email"]}
        access_token = self.create_access_token(token_data)

        # Prepare response
        user_response = UserResponse(**user)
        return AuthResponse(
            user=user_response,
            access_token=access_token,
            expires_in=JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

    async def get_current_user(self, token: str) -> UserResponse:
        """Get current user from JWT token"""

        # Verify token
        payload = self.verify_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )

        # Get user from database
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        user = await db_manager.get_user_by_id_admin(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        return UserResponse(**user)

# Global instance
auth_service = AuthService() 