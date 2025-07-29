"""
Enhanced Weather Chatbot Node - Handles weather-related conversations
Uses multiple weather tools with LLM-driven tool selection
"""

from langchain_core.messages import SystemMessage

def create_enhanced_weather_chatbot_node(llm_with_tools):
    """Create enhanced weather chatbot node with comprehensive weather capabilities"""
    
    # Enhanced weather-specific system prompt
    ENHANCED_WEATHER_PROMPT = """You are an enhanced weather specialist agent with comprehensive weather capabilities.

🌤️ YOUR ROLE:
- You handle ALL weather, climate, and atmospheric questions
- You have access to multiple weather tools for different types of requests
- Choose the most appropriate tool based on the user's specific needs
- Provide helpful, detailed weather information and advice

🔧 AVAILABLE TOOLS:
- get_weather_info: Current weather for a specific city
- get_weather_forecast: Multi-day weather forecast (specify days needed)
- get_climate_data: Historical climate information for a city and month
- compare_weather: Compare current weather between two cities

🎯 EXAMPLES:
- "What's the weather in London?" → Use get_weather_info
- "Give me a 5-day forecast for Tokyo" → Use get_weather_forecast with days=5
- "What's the climate like in Mumbai during July?" → Use get_climate_data
- "Compare weather between New York and Paris" → Use compare_weather
- "Should I pack warm clothes for London?" → Use get_weather_info and provide advice
- "Plan my week in Tokyo" → Use get_weather_forecast for planning advice

Be intelligent about tool selection and provide practical, helpful weather advice."""

    def enhanced_weather_chatbot(state):
        """Enhanced weather chatbot node function"""
        messages = state["messages"].copy()
        
        # Add enhanced weather system prompt
        has_system = any(getattr(msg, 'type', None) == 'system' for msg in messages)
        if not has_system:
            system_msg = SystemMessage(content=ENHANCED_WEATHER_PROMPT)
            messages = [system_msg] + messages
            
        return {"messages": [llm_with_tools.invoke(messages)]}
    
    return enhanced_weather_chatbot 