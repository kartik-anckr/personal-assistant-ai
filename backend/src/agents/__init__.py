"""
Agents module - simplified exports for two-agent system
"""

# Only import the simplified two-agent components
from .weather_agent import create_weather_agent
from .slack_agent import create_slack_agent

# Only export what we need for the simplified system
__all__ = [
    'create_weather_agent',
    'create_slack_agent'
] 