"""
Google Meet Agent State Definitions
"""

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class GoogleMeetState(TypedDict):
    messages: Annotated[list, add_messages] 