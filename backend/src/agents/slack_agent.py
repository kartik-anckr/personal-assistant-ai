"""
Slack Agent - Specialized for sending messages to Slack channels
Handles Slack webhook messaging with channel validation
"""

import os
import importlib.util
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

# Import the Slack messaging tool
from ..tools import send_slack_message, SLACK_CHANNELS

# Import SlackState from states/slack.states directory
_slack_state_path = os.path.join(os.path.dirname(__file__), '..', 'states', 'slack.states', 'slack_state.py')
_spec = importlib.util.spec_from_file_location("slack_state", _slack_state_path)
_slack_state_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_slack_state_module)
SlackState = _slack_state_module.SlackState

# Import nodes and edges from separate modules
from ..nodes import create_slack_chatbot_node
from ..edges import create_slack_workflow_edges

def create_slack_agent():
    """Create a specialized Slack messaging agent"""
    
    print("📱 Creating Slack Agent...")
    
    # Set up Google Gemini 2.0 Flash
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_api_key:
        raise Exception("No Gemini API key found!")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=gemini_api_key,
        temperature=0.2  # Lower temperature for precise messaging
    )
    
    # Slack-specific tools
    slack_tools = [send_slack_message]
    llm_with_tools = llm.bind_tools(slack_tools)
    
    # Get available channels for the prompt
    available_channels = ", ".join(SLACK_CHANNELS.keys())
    
    # Create state graph
    graph_builder = StateGraph(SlackState)
    
    # Create nodes from separate modules
    slack_chatbot_node = create_slack_chatbot_node(llm_with_tools, available_channels)
    
    # Add nodes
    graph_builder.add_node("slack_chatbot", slack_chatbot_node)
    
    tool_node = ToolNode(tools=slack_tools)
    graph_builder.add_node("slack_tools", tool_node)
    
    # Add edges from separate module
    graph_builder = create_slack_workflow_edges(graph_builder)
    
    # Compile
    graph = graph_builder.compile()
    
    print("✅ Slack Agent ready!")
    print(f"📋 Available channels: {available_channels}")
    return graph
