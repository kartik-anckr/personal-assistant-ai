"""
Enhanced Weather Workflow Edges - Defines the weather agent graph connections
Supports multi-step weather analysis with tool looping
"""

from langgraph.graph import START, END
from langgraph.prebuilt import tools_condition

def create_enhanced_weather_workflow_edges(graph_builder):
    """Add enhanced weather workflow edges to the graph builder"""
    
    # Add edges with loopback for multi-step weather analysis
    graph_builder.add_edge(START, "weather_chatbot")
    graph_builder.add_conditional_edges(
        "weather_chatbot",
        tools_condition,
        {"tools": "weather_tools", "__end__": END}
    )
    graph_builder.add_edge("weather_tools", "weather_chatbot")  # Allow multi-step tool usage
    
    return graph_builder 