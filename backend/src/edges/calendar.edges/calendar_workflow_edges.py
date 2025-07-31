"""
Calendar Workflow Edges - Defines calendar agent flow
"""

from langgraph.graph import START, END
from langgraph.prebuilt import tools_condition

def create_calendar_workflow_edges(graph_builder):
    """Add calendar workflow edges to the graph builder"""

    # Start with calendar chatbot
    graph_builder.add_edge(START, "calendar_chatbot")

    # Conditional routing based on tool calls
    graph_builder.add_conditional_edges(
        "calendar_chatbot",
        tools_condition,
        {"tools": "calendar_tools", "__end__": END}
    )

    # After tool execution, end (tools handle the final response)
    graph_builder.add_edge("calendar_tools", END)

    return graph_builder 