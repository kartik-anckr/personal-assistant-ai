"""
Edges module - exports all edge definitions for Simplified Two-Agent System
"""

import importlib.util
import os
import sys

# Import from orchestrator.edges directory  
_orchestrator_edges_dir = os.path.join(os.path.dirname(__file__), 'orchestrator.edges')
sys.path.insert(0, _orchestrator_edges_dir)
try:
    from workflow_edges import create_workflow_edges, create_simplified_workflow_edges, create_legacy_workflow_edges
finally:
    sys.path.remove(_orchestrator_edges_dir)

# Import from slack.edges directory
_slack_edges_dir = os.path.join(os.path.dirname(__file__), 'slack.edges')
sys.path.insert(0, _slack_edges_dir)
try:
    from slack_workflow_edges import create_slack_workflow_edges, create_enhanced_slack_workflow_edges
finally:
    sys.path.remove(_slack_edges_dir)

# Import from weather.edges directory
_weather_edges_dir = os.path.join(os.path.dirname(__file__), 'weather.edges')
sys.path.insert(0, _weather_edges_dir)
try:
    from weather_workflow_edges import create_enhanced_weather_workflow_edges
finally:
    sys.path.remove(_weather_edges_dir)

__all__ = [
    'create_workflow_edges', 
    'create_simplified_workflow_edges',
    'create_legacy_workflow_edges',
    'create_slack_workflow_edges',
    'create_enhanced_slack_workflow_edges',
    'create_enhanced_weather_workflow_edges'
] 