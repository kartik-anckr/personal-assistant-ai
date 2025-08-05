"""
Supabase client configuration and database operations
"""

import os
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Initialize clients as None - will be created when needed
supabase_client: Optional[Client] = None
supabase_admin: Optional[Client] = None

def get_supabase_client() -> Optional[Client]:
    """Get or create Supabase client"""
    global supabase_client
    if supabase_client is None:
        if not SUPABASE_URL or not SUPABASE_ANON_KEY:
            logger.warning("Supabase environment variables not set. Using mock client.")
            return None
        try:
            # Create client with explicit options to avoid proxy argument issue
            options = ClientOptions(
                schema='public',
                headers={'X-Client-Info': 'supabase-py/2.3.4'},
                auto_refresh_token=True,
                persist_session=True
            )
            supabase_client = create_client(
                supabase_url=SUPABASE_URL, 
                supabase_key=SUPABASE_ANON_KEY,
                options=options
            )
        except Exception as e:
            logger.error(f"Failed to create Supabase client: {e}")
            return None
    return supabase_client

def get_supabase_admin() -> Optional[Client]:
    """Get or create Supabase admin client"""
    global supabase_admin
    if supabase_admin is None:
        if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
            logger.warning("Supabase admin environment variables not set. Using mock client.")
            return None
        try:
            # Create admin client with explicit options to avoid proxy argument issue
            options = ClientOptions(
                schema='public',
                headers={'X-Client-Info': 'supabase-py/2.3.4'},
                auto_refresh_token=True,
                persist_session=True
            )
            supabase_admin = create_client(
                supabase_url=SUPABASE_URL, 
                supabase_key=SUPABASE_SERVICE_ROLE_KEY,
                options=options
            )
        except Exception as e:
            logger.error(f"Failed to create Supabase admin client: {e}")
            return None
    return supabase_admin

class SupabaseManager:
    """Manage Supabase database operations"""

    def __init__(self):
        # Clients will be created when first accessed
        pass

    @property
    def client(self) -> Optional[Client]:
        """Get Supabase client (lazy initialization)"""
        return get_supabase_client()

    @property
    def admin(self) -> Optional[Client]:
        """Get Supabase admin client (lazy initialization)"""
        return get_supabase_admin()

    def get_authenticated_client(self, jwt_token: str) -> Optional[Client]:
        """Get Supabase client with user authentication"""
        try:
            if not SUPABASE_URL or not SUPABASE_ANON_KEY:
                return None
                
            # Create client with explicit options
            options = ClientOptions(
                schema='public',
                headers={
                    'X-Client-Info': 'supabase-py/2.3.4',
                    'Authorization': f'Bearer {jwt_token}'
                },
                auto_refresh_token=False,
                persist_session=False
            )
            
            client = create_client(
                supabase_url=SUPABASE_URL,
                supabase_key=SUPABASE_ANON_KEY,
                options=options
            )
            
            # Set the user session with the JWT token
            client.auth.set_session(jwt_token, refresh_token="")
            
            return client
        except Exception as e:
            logger.error(f"Failed to create authenticated Supabase client: {e}")
            return None

    async def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new user in the database"""
        if not self.admin:
            logger.error("Supabase admin client not available. Please configure Supabase environment variables.")
            return None
        try:
            result = self.admin.table('users').insert(user_data).execute()
            if result.data:
                logger.info(f"User created successfully: {user_data['email']}")
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email address"""
        if not self.client:
            logger.error("Supabase client not available. Please configure Supabase environment variables.")
            return None
        try:
            result = self.client.table('users').select("*").eq('email', email).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error fetching user by email: {e}")
            return None

    async def get_user_by_email_admin(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email address using admin client (bypasses RLS)"""
        if not self.admin:
            logger.error("Supabase admin client not available. Please configure Supabase environment variables.")
            return None
        try:
            result = self.admin.table('users').select("*").eq('email', email).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error fetching user by email with admin: {e}")
            return None

    async def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        if not self.client:
            logger.error("Supabase client not available. Please configure Supabase environment variables.")
            return None
        try:
            result = self.client.table('users').select("*").eq('username', username).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error fetching user by username: {e}")
            return None

    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        if not self.client:
            logger.error("Supabase client not available. Please configure Supabase environment variables.")
            return None
        try:
            result = self.client.table('users').select("*").eq('id', user_id).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error fetching user by ID: {e}")
            return None

    async def get_user_by_id_admin(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID using admin client (bypasses RLS)"""
        if not self.admin:
            logger.error("Supabase admin client not available. Please configure Supabase environment variables.")
            return None
        try:
            result = self.admin.table('users').select("*").eq('id', user_id).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error fetching user by ID with admin: {e}")
            return None

    async def update_user(self, user_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update user information"""
        if not self.client:
            logger.error("Supabase client not available. Please configure Supabase environment variables.")
            return None
        try:
            # Add updated_at timestamp
            update_data['updated_at'] = 'NOW()'

            result = self.client.table('users').update(update_data).eq('id', user_id).execute()
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return None

    async def update_last_login(self, user_id: str) -> bool:
        """Update user's last login timestamp"""
        if not self.client:
            logger.error("Supabase client not available. Please configure Supabase environment variables.")
            return False
        try:
            self.client.table('users').update({
                'last_login': 'NOW()'
            }).eq('id', user_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error updating last login: {e}")
            return False

# Global instance
db_manager = SupabaseManager() 