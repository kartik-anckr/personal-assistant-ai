"""
Main package for the Simplified Two-Agent LangGraph System
"""

from .basic_agent import create_agent, chat_with_agent, test_agent

__version__ = "2.0.0"
__all__ = [
    "create_agent",
    "chat_with_agent", 
    "test_agent"
] 