"""
Simplified Orchestrator Workflow Edges - Streamlined flow for two-agent architecture
Removes complex context chains in favor of direct orchestrator → manager pattern
"""

from langgraph.graph import START, END
from langgraph.prebuilt import tools_condition

def create_workflow_edges(graph_builder):
    """Add simplified workflow edges for two-agent architecture"""
    
    # Simplified edges - no complex context chain
    graph_builder.add_edge(START, "orchestrator")
    graph_builder.add_conditional_edges(
        "orchestrator",
        tools_condition,
        {"tools": "manager", "__end__": END}
    )
    graph_builder.add_edge("manager", END)
    
    return graph_builder

# Keep legacy function for backward compatibility
def create_legacy_workflow_edges(graph_builder):
    """Legacy workflow edges - kept for backward compatibility"""
    
    # Add edges - this creates the legacy workflow
    graph_builder.add_edge(START, "orchestrator_with_tools")
    graph_builder.add_conditional_edges(
        "orchestrator_with_tools",
        tools_condition,
        {"tools": "tool_execution", "__end__": "update_context"}
    )
    graph_builder.add_edge("tool_execution", "update_context")
    graph_builder.add_edge("update_context", END)
    
    return graph_builder

# Keep simplified function for new architecture
def create_simplified_workflow_edges(graph_builder):
    """Create simplified workflow edges - new streamlined version"""
    return create_workflow_edges(graph_builder) 