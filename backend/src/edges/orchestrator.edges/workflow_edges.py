"""
Simplified Orchestrator Workflow Edges - Streamlined flow for two-agent architecture
Removes complex context chains in favor of direct orchestrator → manager pattern
"""

from langgraph.graph import START, END
from langgraph.prebuilt import tools_condition

def create_workflow_edges(graph_builder):
    """Add workflow edges for two-agent architecture with orchestrator response formatting
    
    This function defines the workflow flow for an orchestrator that manages
    two specialized agents and formats their responses. The workflow follows this pattern:
    
    START → orchestrator → [conditional] → manager OR END
                ↑                              ↓
                └──────────── orchestrator ←────┘
                                    ↓
                                   END
    
    Flow explanation:
    1. START: Entry point - user input comes in
    2. orchestrator: LLM node that analyzes user intent and decides which agent tool to use
    3. Conditional edge: Based on orchestrator's decision:
       - If tools needed: routes to "manager" (ToolNode that executes agent tools)
       - If no tools needed: goes directly to END
    4. manager: Executes the selected agent tool (invoke_slack_agent or invoke_weather_agent)
    5. orchestrator: Gets tool results and generates friendly, personalized final response
    6. END: Orchestrator's formatted response is returned to user
    
    This ensures the orchestrator can add context, personality, and consistent formatting
    to all agent responses before they reach the user.
    """
    
    # Start workflow at orchestrator node (LLM decision maker)
    graph_builder.add_edge(START, "orchestrator")
    
    # Conditional routing from orchestrator based on tool selection
    # tools_condition automatically checks if LLM wants to call tools
    graph_builder.add_conditional_edges(
        "orchestrator",
        tools_condition,
        {"tools": "manager", "__end__": END}  # Route to manager if tools needed, else END
    )
    
    # After tool execution, come back to orchestrator for response formatting
    graph_builder.add_edge("manager", "orchestrator")
    
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