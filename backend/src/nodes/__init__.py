"""
Nodes module - exports all node definitions
"""

import importlib.util
import os
import sys

# Import from orchestrator.nodes directory  
_orchestrator_nodes_dir = os.path.join(os.path.dirname(__file__), 'orchestrator.nodes')
sys.path.insert(0, _orchestrator_nodes_dir)
try:
    from orchestrator_node import create_orchestrator_node
    from context_update_node import create_context_update_node
finally:
    sys.path.remove(_orchestrator_nodes_dir)

# Import from slack.nodes directory
_slack_nodes_dir = os.path.join(os.path.dirname(__file__), 'slack.nodes')
sys.path.insert(0, _slack_nodes_dir)
try:
    from slack_chatbot_node import create_slack_chatbot_node
finally:
    sys.path.remove(_slack_nodes_dir)

# Import from google_meet.nodes directory
_google_meet_nodes_dir = os.path.join(os.path.dirname(__file__), 'google_meet.nodes')
sys.path.insert(0, _google_meet_nodes_dir)
try:
    from google_meet_chatbot_node import create_google_meet_chatbot_node
finally:
    sys.path.remove(_google_meet_nodes_dir)

__all__ = ['create_orchestrator_node', 'create_context_update_node', 'create_slack_chatbot_node', 'create_google_meet_chatbot_node'] 