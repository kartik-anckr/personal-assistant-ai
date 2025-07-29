"""
Orchestrator V2 Workflow State Definition
"""

from typing import Annotated, Dict, Any
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class SimpleWorkflowState(TypedDict):
    messages: Annotated[list, add_messages]
    agent_results: Dict[str, str]  # Store results from different agents
    context: str  # Simple context passing 