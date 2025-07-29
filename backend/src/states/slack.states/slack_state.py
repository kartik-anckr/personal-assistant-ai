"""
Slack Agent State Definitions
"""

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class SlackState(TypedDict):
    messages: Annotated[list, add_messages] 