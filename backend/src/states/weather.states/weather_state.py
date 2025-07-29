"""
Weather State Definition - State structure for the enhanced weather agent
"""

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class WeatherState(TypedDict):
    """State definition for the enhanced weather agent"""
    messages: Annotated[list, add_messages] 