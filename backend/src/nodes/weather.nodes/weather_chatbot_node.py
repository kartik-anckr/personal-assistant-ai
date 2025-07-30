"""
Enhanced Weather Chatbot Node - Handles weather-related conversations
Uses multiple weather tools with LLM-driven tool selection
"""

from langchain_core.messages import SystemMessage, ToolMessage
import sys
import os

# Import weather tools for execution
_weather_tools_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'weather.tools')
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

    # Create a mapping of tool names to actual functions
    tool_map = {
        'get_weather_info': get_weather_info,
        'get_weather_forecast': get_weather_forecast, 
        'get_climate_data': get_climate_data,
        'compare_weather': compare_weather
    }

    def enhanced_weather_chatbot(state):
        """Enhanced weather chatbot node function with proper tool execution"""
        messages = state["messages"].copy()
        
        # Add enhanced weather system prompt
        has_system = any(getattr(msg, 'type', None) == 'system' for msg in messages)
        if not has_system:
            system_msg = SystemMessage(content=ENHANCED_WEATHER_PROMPT)
            messages = [system_msg] + messages
        
        # Get LLM response (may include tool calls)
        response = llm_with_tools.invoke(messages)

        print(f"🌤️ [ENHANCED WEATHER CHATBOT] Response: {response}")
        print(f"🌤️ [ENHANCED WEATHER CHATBOT] Tool calls: {response.tool_calls}")
        
        # Check if the response contains tool calls
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"🔧 Weather agent executing {len(response.tool_calls)} tool(s)")
            
            # Add the LLM's response with tool calls to messages
            messages.append(response)
            
            # Execute each tool call
            for tool_call in response.tool_calls:
                tool_name = tool_call['name']
                tool_args = tool_call['args']
                tool_id = tool_call['id']
                
                print(f"🌤️ Executing tool: {tool_name} with args: {tool_args}")
                
                try:
                    # Execute the tool
                    if tool_name in tool_map:
                        tool_result = tool_map[tool_name].invoke(tool_args)
                        print(f"✅ Tool {tool_name} result: {tool_result}")
                    else:
                        tool_result = f"Error: Unknown tool {tool_name}"
                        print(f"❌ Unknown tool: {tool_name}")
                    
                    # Add tool result as a ToolMessage
                    tool_message = ToolMessage(
                        content=str(tool_result),
                        tool_call_id=tool_id,
                        name=tool_name
                    )
                    messages.append(tool_message)
                    
                except Exception as e:
                    error_msg = f"Error executing {tool_name}: {str(e)}"
                    print(f"❌ {error_msg}")
                    tool_message = ToolMessage(
                        content=error_msg,
                        tool_call_id=tool_id,
                        name=tool_name
                    )
                    messages.append(tool_message)
            
            # Get final response from LLM with tool results
            final_response = llm_with_tools.invoke(messages)
            return {"messages": [final_response]}
        else:
            # No tool calls, return the response directly
            return {"messages": [response]}
    
    return enhanced_weather_chatbot 