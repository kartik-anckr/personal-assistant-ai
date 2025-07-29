"""
Google Meet Workflow Edges - Defines the Google Meet agent graph edges and connections
"""

from langgraph.graph import START, END
from langgraph.prebuilt import tools_condition

def create_google_meet_workflow_edges(graph_builder):
    """Add all Google Meet workflow edges to the graph builder"""
    
    # Add edges
    graph_builder.add_edge(START, "google_meet_chatbot")
    graph_builder.add_conditional_edges(
        "google_meet_chatbot",
        tools_condition,
        {"tools": "google_meet_tools", "__end__": END}
    )
    graph_builder.add_edge("google_meet_tools", "google_meet_chatbot")
    
    return graph_builder 