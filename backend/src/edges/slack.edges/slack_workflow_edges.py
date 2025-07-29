"""
Slack Workflow Edges - Defines the slack agent graph edges and connections
"""

from langgraph.graph import START, END
from langgraph.prebuilt import tools_condition

def create_slack_workflow_edges(graph_builder):
    """Add all slack workflow edges to the graph builder"""
    
    # Add edges
    graph_builder.add_edge(START, "slack_chatbot")
    graph_builder.add_conditional_edges(
        "slack_chatbot",
        tools_condition,
        {"tools": "slack_tools", "__end__": END}
    )
    graph_builder.add_edge("slack_tools", "slack_chatbot")
    
    return graph_builder 