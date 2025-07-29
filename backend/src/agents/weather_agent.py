"""
Weather Agent - Specialized for weather-related queries
Handles weather information, forecasts, and climate questions
"""

import os
from typing import Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage

# Weather-specific tool
@tool
def get_weather_info(city: str) -> str:
    """Get current weather information for a city.
    
    Args:
        city: Name of the city
        
    Returns:
        Weather information for the city
    """
    # Mock weather data (in real app, would call actual weather API)
    weather_data = {
        "new york": "🌤️ Partly cloudy, 22°C, light breeze",
        "london": "🌧️ Rainy, 15°C, moderate wind", 
        "tokyo": "☀️ Sunny, 28°C, clear skies",
        "paris": "⛅ Overcast, 18°C, calm",
        "sydney": "🌞 Bright and sunny, 25°C, gentle breeze",
        "mumbai": "🌦️ Monsoon season, 26°C, heavy rain expected"
    }
    
    city_lower = city.lower()
    weather = weather_data.get(city_lower, f"🌍 Weather data for {city} not available in demo")
    
    print(f"🌤️ Weather tool used for: {city} → {weather}")
    return weather

class WeatherState(TypedDict):
    messages: Annotated[list, add_messages]

def create_weather_agent():
    """Create a specialized weather agent"""
    
    print("🌤️ Creating Weather Agent...")
    
    # Set up Google Gemini 2.0 Flash
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_api_key:
        raise Exception("No Gemini API key found!")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=gemini_api_key,
        temperature=0.7  # More creative for weather descriptions
    )
    
    # Weather-specific tools
    weather_tools = [get_weather_info]
    llm_with_tools = llm.bind_tools(weather_tools)
    
    # Weather-specific system prompt
    WEATHER_PROMPT = """You are a specialized weather agent. Your expertise is weather and climate information.

🌤️ YOUR ROLE:
- You ONLY handle weather, climate, and atmospheric questions
- Use get_weather_info tool when users ask about specific city weather
- Provide helpful weather-related advice and information
- Be friendly and informative about weather conditions

🎯 EXAMPLES:
- "What's the weather in London?" → Use get_weather_info tool
- "How's the weather in Tokyo today?" → Use get_weather_info tool
- "Should I carry an umbrella?" → Give general weather advice
- "What's a good weather app?" → Provide weather-related recommendations

Be helpful, weather-focused, and provide practical weather advice."""

    # Create state graph
    graph_builder = StateGraph(WeatherState)
    
    def weather_chatbot(state: WeatherState):
        messages = state["messages"].copy()
        
        # Add weather system prompt
        has_system = any(getattr(msg, 'type', None) == 'system' for msg in messages)
        if not has_system:
            system_msg = SystemMessage(content=WEATHER_PROMPT)
            messages = [system_msg] + messages
            
        return {"messages": [llm_with_tools.invoke(messages)]}
    
    # Add nodes
    graph_builder.add_node("weather_chatbot", weather_chatbot)
    
    tool_node = ToolNode(tools=weather_tools)
    graph_builder.add_node("weather_tools", tool_node)
    
    # Add edges
    graph_builder.add_edge(START, "weather_chatbot")
    graph_builder.add_conditional_edges(
        "weather_chatbot",
        tools_condition,
        {"tools": "weather_tools", "__end__": END}
    )
    graph_builder.add_edge("weather_tools", "weather_chatbot")
    
    # Compile
    graph = graph_builder.compile()
    
    print("✅ Weather Agent ready!")
    return graph

async def chat_with_weather_agent(agent, user_input: str):
    """Chat with the weather agent"""
    print(f"🌤️ [WEATHER AGENT] Processing: {user_input}")
    
    result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
    response = result["messages"][-1].content
    
    print(f"🌤️ [WEATHER AGENT] Result: {response}")
    return response 