"""
Enhanced Weather Agent - Uses modular components for tools, nodes, edges, and state
Handles weather information, forecasts, climate data, and weather comparisons
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
from langgraph.prebuilt import ToolNode

from ..nodes import create_enhanced_weather_chatbot_node
from ..edges import create_enhanced_weather_workflow_edges

def create_weather_agent():
    """Create an enhanced weather agent using modular components"""
    
    print("🌤️ Creating Enhanced Weather Agent...")
    
    # Set up Google Gemini 2.0 Flash
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_api_key:
        raise Exception("No Gemini API key found!")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=gemini_api_key,
        temperature=0.7  # More creative for weather descriptions
    )
    
    # Enhanced weather tools - multiple tools for comprehensive weather capabilities
    weather_tools = [
        get_weather_info,
        get_weather_forecast, 
        get_climate_data,
        compare_weather
    ]
    llm_with_tools = llm.bind_tools(weather_tools)
    
    # Create state graph using modular components
    graph_builder = StateGraph(WeatherState)
    
    # Add nodes using modular components
    weather_chatbot_node = create_enhanced_weather_chatbot_node(llm_with_tools)
    graph_builder.add_node("weather_chatbot", weather_chatbot_node)
    
    tool_node = ToolNode(tools=weather_tools)
    graph_builder.add_node("weather_tools", tool_node)
    
    # Add edges using modular components
    graph_builder = create_enhanced_weather_workflow_edges(graph_builder)
    
    # Compile
    graph = graph_builder.compile()
    
    print("✅ Enhanced Weather Agent ready!")
    print("🔧 Available tools: current weather, forecasts, climate data, weather comparison")
    return graph

async def chat_with_weather_agent(agent, user_input: str):
    """Chat with the enhanced weather agent"""
    print(f"🌤️ [ENHANCED WEATHER AGENT] Processing: {user_input}")
    
    result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
    response = result["messages"][-1].content
    
    print(f"🌤️ [ENHANCED WEATHER AGENT] Result: {response}")
    return response 