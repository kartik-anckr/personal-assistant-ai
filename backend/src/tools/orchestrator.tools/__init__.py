"""
Orchestrator tools module
"""

from .math_agent_tool import create_math_agent_tool
from .weather_agent_tool import create_weather_agent_tool
from .slack_agent_tool import create_slack_agent_tool

def create_orchestrator_tools(arithmetic_agent, weather_agent, slack_agent):
    """Create all orchestrator tools"""
    
    math_tool = create_math_agent_tool(arithmetic_agent)
    weather_tool = create_weather_agent_tool(weather_agent)
    slack_tool = create_slack_agent_tool(slack_agent)
    
    return [math_tool, weather_tool, slack_tool]

__all__ = [
    'create_math_agent_tool',
    'create_weather_agent_tool', 
    'create_slack_agent_tool',
    'create_orchestrator_tools'
] 