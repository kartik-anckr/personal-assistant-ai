"""
Database module for Supabase integration
"""

from .supabase_client import SupabaseManager, db_manager

__all__ = ['SupabaseManager', 'db_manager'] 