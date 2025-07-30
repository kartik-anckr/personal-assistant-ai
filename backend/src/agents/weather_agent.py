"""
Enhanced Weather Agent (Simplified) - No ToolNode
LLM directly uses bound weather tools within a single node
"""

import sys
import os
_weather_tools_dir = os.path.join(os.path.dirname(__file__), '..', 'tools', 'weather.tools')
sys.path.insert(0, _weather_tools_dir)
try:
    from enhanced_weather_tools import (
        get_weather_info,
        get_weather_forecast,
        get_climate_data,
        compare_weather
    )
finally:
    sys.path.remove(_weather_tools_dir)

import importlib.util
_weather_state_path = os.path.join(os.path.dirname(__file__), '..', 'states', 'weather.states', 'weather_state.py')
_spec = importlib.util.spec_from_file_location("weather_state", _weather_state_path)
_weather_state_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_weather_state_module)
WeatherState = _weather_state_module.WeatherState

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph
from langgraph.graph import START, END

from ..nodes import create_enhanced_weather_chatbot_node

def create_weather_agent():
    """Create an enhanced weather agent without ToolNode"""
    print("🌤️ Creating Simplified Enhanced Weather Agent...")

    # API key check
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise Exception("No Gemini API key found!")

    # LLM setup
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=gemini_api_key,
        temperature=0.7
    )

    # Bind tools directly to LLM
    weather_tools = [
        get_weather_info,
        get_weather_forecast,
        get_climate_data,
        compare_weather
    ]
    llm_with_tools = llm.bind_tools(weather_tools)

    # Build graph
    graph_builder = StateGraph(WeatherState)

    # Only one node needed
    weather_chatbot_node = create_enhanced_weather_chatbot_node(llm_with_tools)
    graph_builder.add_node("weather_chatbot", weather_chatbot_node)

    # Simple edges: start → chatbot → end
    graph_builder.add_edge(START, "weather_chatbot")
    graph_builder.add_edge("weather_chatbot", END)

    # Compile and return
    graph = graph_builder.compile()

    print("✅ Simplified Enhanced Weather Agent ready!")
    return graph


# Chat method (same as before)
async def chat_with_weather_agent(agent, user_input: str):
    """Chat with the enhanced weather agent"""
    print(f"🌤️ [ENHANCED WEATHER AGENT] Processing: {user_input}")

    result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
    response = result["messages"][-1].content

    print(f"🌤️ [ENHANCED WEATHER AGENT] Result: {response}")
    return response
