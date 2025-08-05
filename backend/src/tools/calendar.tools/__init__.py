"""
Calendar tools module
"""

import os
import sys
import importlib.util

# Load calendar_tools directly
calendar_tools_path = os.path.join(os.path.dirname(__file__), 'calendar_tools.py')
if os.path.exists(calendar_tools_path):
    spec = importlib.util.spec_from_file_location("calendar_tools", calendar_tools_path)
    calendar_tools_module = importlib.util.module_from_spec(spec)
    sys.modules['calendar_tools'] = calendar_tools_module
    spec.loader.exec_module(calendar_tools_module)
    
    create_calendar_tools = calendar_tools_module.create_calendar_tools
    create_calendar_event = calendar_tools_module.create_calendar_event
    get_upcoming_meetings_tool = calendar_tools_module.get_upcoming_meetings_tool
else:
    # Create dummy functions if file doesn't exist
    def create_calendar_tools():
        return []
    def create_calendar_event(prompt: str, user_id: str) -> str:
        return "❌ Calendar tools not available due to import error."
    def get_upcoming_meetings_tool(query: str = "next 7 days", user_id: str = None) -> str:
        return "❌ Upcoming meetings not available due to import error."

# Load upcoming_meetings_tool directly
upcoming_meetings_tool_path = os.path.join(os.path.dirname(__file__), 'upcoming_meetings_tool.py')
if os.path.exists(upcoming_meetings_tool_path):
    spec = importlib.util.spec_from_file_location("upcoming_meetings_tool", upcoming_meetings_tool_path)
    upcoming_meetings_module = importlib.util.module_from_spec(spec)
    sys.modules['upcoming_meetings_tool'] = upcoming_meetings_module
    spec.loader.exec_module(upcoming_meetings_module)
    
    get_upcoming_meetings = upcoming_meetings_module.get_upcoming_meetings
else:
    async def get_upcoming_meetings(query: str = "next 7 days", user_id: str = None) -> str:
        return "❌ Upcoming meetings not available due to import error."

__all__ = ['create_calendar_tools', 'create_calendar_event', 'get_upcoming_meetings_tool', 'get_upcoming_meetings'] 