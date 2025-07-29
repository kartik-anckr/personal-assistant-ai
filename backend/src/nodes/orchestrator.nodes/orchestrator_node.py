"""
Simplified Orchestrator Node - LLM-driven agent selection for two-agent architecture
Focuses on Slack and Weather agents with intelligent routing
"""

from langchain_core.messages import SystemMessage

def create_orchestrator_node(llm_with_tools):
    """Create the simplified orchestrator node for two-agent architecture"""
    
    # Enhanced system prompt for two-agent selection
    SIMPLIFIED_SYSTEM_PROMPT = """You are an intelligent task orchestrator with access to two specialized agents:

🔧 AVAILABLE TOOLS:
- invoke_slack_agent: For Slack messaging, reading messages, channel management, and communication tasks
- invoke_weather_agent: For weather information, forecasts, climate data, and weather-related queries

🎯 YOUR JOB:
Analyze the user's request and automatically select the appropriate agent tool based on intent.
You do NOT need keyword matching or pattern recognition - use natural language understanding.

EXAMPLES:
- "Send hello to team channel" → invoke_slack_agent
- "What channels are available in Slack?" → invoke_slack_agent  
- "Read recent messages from development channel" → invoke_slack_agent
- "Weather in London?" → invoke_weather_agent
- "Give me a 5-day forecast for Tokyo" → invoke_weather_agent
- "Compare weather between NYC and LA" → invoke_weather_agent

Let your LLM intelligence guide tool selection naturally. Choose the most appropriate agent for the user's intent."""

    def simplified_orchestrator_with_tools(state):
        """Simplified orchestrator node with enhanced LLM decision making"""
        messages = state["messages"].copy()
        
        # Add enhanced system prompt
        has_system = any(getattr(msg, 'type', None) == 'system' for msg in messages)
        if not has_system:
            system_msg = SystemMessage(content=SIMPLIFIED_SYSTEM_PROMPT)
            messages = [system_msg] + messages
        
        # Add context from previous agent results if available
        if state.get("context"):
            context_info = f"\nPrevious context: {state['context']}"
            if messages and hasattr(messages[-1], 'content'):
                messages[-1].content += context_info
        
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}
    
    return simplified_orchestrator_with_tools

# Keep backward compatibility with original function name
def create_simplified_orchestrator_node(llm_with_tools):
    """Create simplified orchestrator node - new enhanced version"""
    return create_orchestrator_node(llm_with_tools) 