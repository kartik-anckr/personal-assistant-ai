"""
Google Meet Agent - Specialized for scheduling Google Meet meetings
Handles Google Calendar API integration with automatic Meet link generation
"""

import os
import importlib.util
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

# Import the Google Meet scheduling tool
from ..tools import schedule_google_meet

# Import GoogleMeetState from states/google_meet.states directory
_google_meet_state_path = os.path.join(os.path.dirname(__file__), '..', 'states', 'google_meet.states', 'google_meet_state.py')
_spec = importlib.util.spec_from_file_location("google_meet_state", _google_meet_state_path)
_google_meet_state_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_google_meet_state_module)
GoogleMeetState = _google_meet_state_module.GoogleMeetState

# Import nodes and edges from separate modules
from ..nodes import create_google_meet_chatbot_node
from ..edges import create_google_meet_workflow_edges

def create_google_meet_agent():
    """Create a specialized Google Meet scheduling agent"""
    
    print("📅 Creating Google Meet Agent...")
    
    # Set up Google Gemini 2.0 Flash
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_api_key:
        raise Exception("No Gemini API key found!")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=gemini_api_key,
        temperature=0.3  # Balanced temperature for scheduling accuracy and natural language understanding
    )
    
    # Google Meet-specific tools
    google_meet_tools = [schedule_google_meet]
    llm_with_tools = llm.bind_tools(google_meet_tools)
    
    # Create state graph
    graph_builder = StateGraph(GoogleMeetState)
    
    # Create nodes from separate modules
    google_meet_chatbot_node = create_google_meet_chatbot_node(llm_with_tools)
    
    # Add nodes
    graph_builder.add_node("google_meet_chatbot", google_meet_chatbot_node)
    
    tool_node = ToolNode(tools=google_meet_tools)
    graph_builder.add_node("google_meet_tools", tool_node)
    
    # Add edges from separate module
    graph_builder = create_google_meet_workflow_edges(graph_builder)
    
    # Compile
    graph = graph_builder.compile()
    
    print("✅ Google Meet Agent ready!")
    print("📅 Capabilities: Meeting scheduling, Google Calendar integration, automatic Meet links")
    return graph 