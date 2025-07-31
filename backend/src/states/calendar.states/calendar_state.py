"""
Calendar Agent State Definition
"""

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class CalendarState(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str  # Track which user is making the request 