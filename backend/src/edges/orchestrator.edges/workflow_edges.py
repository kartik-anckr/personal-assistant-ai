"""
Orchestrator Workflow Edges - Defines the graph edges and connections
"""

from langgraph.graph import START, END
from langgraph.prebuilt import tools_condition

def create_workflow_edges(graph_builder):
    """Add all workflow edges to the graph builder"""
    
    # Add edges - this creates the V2 workflow
    graph_builder.add_edge(START, "orchestrator_with_tools")
    graph_builder.add_conditional_edges(
        "orchestrator_with_tools",
        tools_condition,
        {"tools": "tool_execution", "__end__": "update_context"}
    )
    graph_builder.add_edge("tool_execution", "update_context")
    graph_builder.add_edge("update_context", END)
    
    return graph_builder 