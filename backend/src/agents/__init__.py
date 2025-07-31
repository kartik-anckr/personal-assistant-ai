"""
Agents module - simplified exports for two-agent system
"""

# Import all three agent components
from .weather_agent import create_weather_agent
from .slack_agent import create_slack_agent
from .calendar_agent import create_calendar_agent

# Export all agents for the three-agent system
__all__ = [
    'create_weather_agent',
    'create_slack_agent',
    'create_calendar_agent'
] 