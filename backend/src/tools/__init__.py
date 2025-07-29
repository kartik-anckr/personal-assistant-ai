"""
Enhanced tools module - exports all available tools for Simplified Two-Agent System
Includes enhanced Slack and Weather capabilities only
"""

import importlib.util
import os

# Import enhanced slack tools from the slack.tools directory
_slack_tools_path = os.path.join(os.path.dirname(__file__), 'slack.tools', 'slack_messaging.py')
_spec = importlib.util.spec_from_file_location("slack_messaging", _slack_tools_path)
_slack_messaging = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_slack_messaging)

# Export all enhanced slack tools
send_slack_message = _slack_messaging.send_slack_message
read_slack_messages = _slack_messaging.read_slack_messages
list_slack_channels = _slack_messaging.list_slack_channels
get_channel_info = _slack_messaging.get_channel_info
SLACK_CHANNELS = _slack_messaging.SLACK_CHANNELS

# Import enhanced weather tools from the weather.tools directory
_weather_tools_path = os.path.join(os.path.dirname(__file__), 'weather.tools', 'enhanced_weather_tools.py')
_spec = importlib.util.spec_from_file_location("enhanced_weather_tools", _weather_tools_path)
_weather_tools = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_weather_tools)

# Export all enhanced weather tools
get_weather_info = _weather_tools.get_weather_info
get_weather_forecast = _weather_tools.get_weather_forecast
get_climate_data = _weather_tools.get_climate_data
compare_weather = _weather_tools.compare_weather

# Import simplified orchestrator tools from orchestrator.tools directory
import sys
_tools_dir = os.path.join(os.path.dirname(__file__), 'orchestrator.tools')
sys.path.insert(0, _tools_dir)
try:
    from weather_agent_tool import create_weather_agent_tool
    from slack_agent_tool import create_slack_agent_tool
    
    # Import the simplified orchestrator tools creation function
    def create_simplified_orchestrator_tools(slack_agent, weather_agent):
        """Create simplified orchestrator tools - only 2 agent invocation tools"""
        
        # Create agent invocation tools with new names
        slack_tool = create_slack_agent_tool(slack_agent)
        weather_tool = create_weather_agent_tool(weather_agent)
        
        # Rename tools to match the simplified architecture
        slack_tool.name = "invoke_slack_agent"
        slack_tool.description = "Handle Slack-related requests including messaging, reading messages, and channel management"
        
        weather_tool.name = "invoke_weather_agent" 
        weather_tool.description = "Handle weather-related requests including current weather, forecasts, and climate data"
        
        return [slack_tool, weather_tool]
    
    # Keep legacy function for backward compatibility
    def create_orchestrator_tools(arithmetic_agent=None, weather_agent=None, slack_agent=None, google_meet_agent=None):
        """Legacy orchestrator tools function - kept for backward compatibility"""
        if slack_agent and weather_agent:
            return create_simplified_orchestrator_tools(slack_agent, weather_agent)
        else:
            raise Exception("Simplified orchestrator only supports Slack and Weather agents")
            
finally:
    sys.path.remove(_tools_dir)

__all__ = [
    # Enhanced Slack tools
    'send_slack_message', 
    'read_slack_messages',
    'list_slack_channels',
    'get_channel_info',
    'SLACK_CHANNELS',
    
    # Enhanced Weather tools
    'get_weather_info',
    'get_weather_forecast',
    'get_climate_data',
    'compare_weather',
    
    # Orchestrator functions
    'create_simplified_orchestrator_tools',
    'create_orchestrator_tools'
] 