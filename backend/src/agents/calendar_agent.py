"""
Google Calendar Agent - Handles calendar event creation through natural language
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
from langgraph.graph import START, END
import os
import importlib.util

# Import CalendarState from states/calendar.states directory
_calendar_state_path = os.path.join(os.path.dirname(__file__), '..', 'states', 'calendar.states', 'calendar_state.py')
_spec = importlib.util.spec_from_file_location("calendar_state", _calendar_state_path)
_calendar_state_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_calendar_state_module)
CalendarState = _calendar_state_module.CalendarState

# Import calendar tools
import sys
_tools_dir = os.path.join(os.path.dirname(__file__), '..', 'tools', 'calendar.tools')
sys.path.insert(0, _tools_dir)
try:
    from calendar_tools import create_calendar_tools
finally:
    sys.path.remove(_tools_dir)

# Import calendar chatbot node
_nodes_dir = os.path.join(os.path.dirname(__file__), '..', 'nodes', 'calendar.nodes')
sys.path.insert(0, _nodes_dir)
try:
    from calendar_chatbot_node import create_calendar_chatbot_node
finally:
    sys.path.remove(_nodes_dir)

def create_calendar_agent():
    """Create simplified Google Calendar agent without ToolNode"""
    print("📅 Creating Simplified Google Calendar Agent...")

    # Create LLM for calendar operations
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise Exception("No Gemini API key found for Calendar Agent!")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=gemini_api_key,
        temperature=0.1  # Lower temperature for more precise calendar operations
    )

    # Create calendar tools and bind directly to LLM
    calendar_tools = create_calendar_tools()
    llm_with_tools = llm.bind_tools(calendar_tools)

    # Build simplified graph
    graph_builder = StateGraph(CalendarState)

    # Only one node needed - calendar chatbot handles everything
    calendar_chatbot_node = create_calendar_chatbot_node(llm_with_tools)
    graph_builder.add_node("calendar_chatbot", calendar_chatbot_node)

    # Simple edges: start → calendar_chatbot → end
    graph_builder.add_edge(START, "calendar_chatbot")
    graph_builder.add_edge("calendar_chatbot", END)

    # Compile and return
    graph = graph_builder.compile()

    print("✅ Simplified Google Calendar Agent ready!")
    return graph

# Chat function for testing
async def chat_with_calendar_agent(agent, user_input: str, user_id: str = None):
    """Chat with calendar agent for testing"""
    print(f"\n📅 [CALENDAR AGENT] Processing: {user_input}")

    initial_state = {
        "messages": [{"role": "user", "content": user_input}],
        "user_id": user_id
    }
    result = agent.invoke(initial_state)

    final_message = result["messages"][-1]
    response = final_message.content if hasattr(final_message, 'content') else str(final_message)

    print(f"📅 [CALENDAR AGENT] Response: {response}")
    return response 