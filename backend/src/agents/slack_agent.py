"""
Enhanced Slack Agent - Uses modular components for tools, nodes, edges, and state  
Handles Slack messaging, reading, channel management, and communication tasks
"""

import os
import importlib.util
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
from langgraph.graph import START, END

# Import only the send message tool
from ..tools import (
    send_slack_message,
    SLACK_CHANNELS
)

# Import SlackState from states/slack.states directory
_slack_state_path = os.path.join(os.path.dirname(__file__), '..', 'states', 'slack.states', 'slack_state.py')
_spec = importlib.util.spec_from_file_location("slack_state", _slack_state_path)
_slack_state_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_slack_state_module)
SlackState = _slack_state_module.SlackState

# Import nodes from modular components
from ..nodes import create_enhanced_slack_chatbot_node

def create_slack_agent():
    """Create a simplified Slack agent with direct tool binding"""
    
    print("📱 Creating Simplified Slack Agent...")
    
    # Set up Google Gemini 2.0 Flash
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_api_key:
        raise Exception("No Gemini API key found!")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=gemini_api_key,
        temperature=0.2  # Lower temperature for precise messaging
    )
    
    # Simplified Slack tools - only send message tool
    slack_tools = [
        send_slack_message
    ]
    llm_with_tools = llm.bind_tools(slack_tools)
    
    # Get available channels for the prompt
    available_channels = ", ".join(SLACK_CHANNELS.keys())
    
    # Create state graph
    graph_builder = StateGraph(SlackState)
    
    # Only one node needed
    slack_chatbot_node = create_enhanced_slack_chatbot_node(llm_with_tools, available_channels)
    graph_builder.add_node("slack_chatbot", slack_chatbot_node)
    
    # Simple edges: start → chatbot → end
    graph_builder.add_edge(START, "slack_chatbot")
    graph_builder.add_edge("slack_chatbot", END)
    
    # Compile
    graph = graph_builder.compile()
    
    print("✅ Simplified Slack Agent ready!")
    print(f"📋 Available channels: {available_channels}")
    print("🔧 Available tools: send messages")
    return graph
