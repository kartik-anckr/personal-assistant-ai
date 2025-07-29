"""
Enhanced Slack Workflow Edges - Defines the slack agent graph connections
Supports multi-step Slack operations with tool looping
"""

from langgraph.graph import START, END
from langgraph.prebuilt import tools_condition

def create_slack_workflow_edges(graph_builder):
    """Add enhanced slack workflow edges to the graph builder"""
    
    # Add edges with loopback for multi-step Slack operations
    graph_builder.add_edge(START, "slack_chatbot")
    graph_builder.add_conditional_edges(
        "slack_chatbot",
        tools_condition,
        {"tools": "slack_tools", "__end__": END}
    )
    graph_builder.add_edge("slack_tools", "slack_chatbot")  # Allow multi-step tool usage
    
    return graph_builder

# Keep backward compatibility
def create_enhanced_slack_workflow_edges(graph_builder):
    """Create enhanced slack workflow edges - new enhanced version"""
    return create_slack_workflow_edges(graph_builder) 