"""
Simplified orchestrator tools module - Only Slack and Weather agents
"""

from .weather_agent_tool import create_weather_agent_tool
from .slack_agent_tool import create_slack_agent_tool

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

__all__ = [
    'create_weather_agent_tool', 
    'create_slack_agent_tool',
    'create_simplified_orchestrator_tools'
] 