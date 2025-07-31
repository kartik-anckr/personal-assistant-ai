"""
Nodes module - exports all node definitions for Simplified Two-Agent System
"""

import importlib.util
import os
import sys

# Import from orchestrator.nodes directory  
_orchestrator_nodes_dir = os.path.join(os.path.dirname(__file__), 'orchestrator.nodes')
sys.path.insert(0, _orchestrator_nodes_dir)
try:
    from orchestrator_node import create_orchestrator_node, create_simplified_orchestrator_node
    from context_update_node import create_context_update_node
finally:
    sys.path.remove(_orchestrator_nodes_dir)

# Import from slack.nodes directory
_slack_nodes_dir = os.path.join(os.path.dirname(__file__), 'slack.nodes')
sys.path.insert(0, _slack_nodes_dir)
try:
    from slack_chatbot_node import create_slack_chatbot_node, create_enhanced_slack_chatbot_node
finally:
    sys.path.remove(_slack_nodes_dir)

# Import from weather.nodes directory
_weather_nodes_dir = os.path.join(os.path.dirname(__file__), 'weather.nodes')
sys.path.insert(0, _weather_nodes_dir)
try:
    from weather_chatbot_node import create_enhanced_weather_chatbot_node
finally:
    sys.path.remove(_weather_nodes_dir)

# Import from calendar.nodes directory
_calendar_nodes_dir = os.path.join(os.path.dirname(__file__), 'calendar.nodes')
sys.path.insert(0, _calendar_nodes_dir)
try:
    from calendar_chatbot_node import create_calendar_chatbot_node
finally:
    sys.path.remove(_calendar_nodes_dir)

__all__ = [
    'create_orchestrator_node', 
    'create_simplified_orchestrator_node',
    'create_context_update_node', 
    'create_slack_chatbot_node',
    'create_enhanced_slack_chatbot_node',
    'create_enhanced_weather_chatbot_node',
    'create_calendar_chatbot_node'
] 