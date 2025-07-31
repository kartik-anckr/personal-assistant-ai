"""
Google Calendar Agent - Handles calendar event creation through natural language
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
import os
import importlib.util

# Import CalendarState from states/calendar.states directory
_calendar_state_path = os.path.join(os.path.dirname(__file__), '..', 'states', 'calendar.states', 'calendar_state.py')
_spec = importlib.util.spec_from_file_location("calendar_state", _calendar_state_path)
_calendar_state_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_calendar_state_module)
CalendarState = _calendar_state_module.CalendarState

# Import modular components using the same pattern as other agents
import sys
_tools_dir = os.path.join(os.path.dirname(__file__), '..', 'tools', 'calendar.tools')
sys.path.insert(0, _tools_dir)
try:
    from calendar_tools import create_calendar_tools
finally:
    sys.path.remove(_tools_dir)

_nodes_dir = os.path.join(os.path.dirname(__file__), '..', 'nodes', 'calendar.nodes')
sys.path.insert(0, _nodes_dir)
try:
    from calendar_chatbot_node import create_calendar_chatbot_node
finally:
    sys.path.remove(_nodes_dir)

_edges_dir = os.path.join(os.path.dirname(__file__), '..', 'edges', 'calendar.edges')
sys.path.insert(0, _edges_dir)
try:
    from calendar_workflow_edges import create_calendar_workflow_edges
finally:
    sys.path.remove(_edges_dir)

def create_calendar_agent():
    """Create Google Calendar agent graph"""
    print("🔧 Creating Google Calendar Agent...")

    # Create LLM for calendar operations
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise Exception("No Gemini API key found for Calendar Agent!")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=gemini_api_key,
        temperature=0.1  # Lower temperature for more precise calendar operations
    )

    # Create calendar tools
    calendar_tools = create_calendar_tools()
    llm_with_tools = llm.bind_tools(calendar_tools)

    # Create calendar agent graph
    graph_builder = StateGraph(CalendarState)

    # Add nodes
    calendar_chatbot = create_calendar_chatbot_node(llm_with_tools)
    graph_builder.add_node("calendar_chatbot", calendar_chatbot)
    graph_builder.add_node("calendar_tools", ToolNode(tools=calendar_tools))

    # Add edges
    graph_builder = create_calendar_workflow_edges(graph_builder)

    # Compile graph
    graph = graph_builder.compile()

    print("✅ Google Calendar Agent ready!")
    return graph

# Chat function for testing
async def chat_with_calendar_agent(agent, user_input: str):
    """Chat with calendar agent for testing"""
    print(f"\n📅 [CALENDAR AGENT] Processing: {user_input}")

    initial_state = {"messages": [{"role": "user", "content": user_input}]}
    result = agent.invoke(initial_state)

    final_message = result["messages"][-1]
    response = final_message.content if hasattr(final_message, 'content') else str(final_message)

    print(f"📅 [CALENDAR AGENT] Response: {response}")
    return response 