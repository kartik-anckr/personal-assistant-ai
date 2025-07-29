"""
Orchestrator Node - Main orchestrator node with tool capabilities
"""

from langchain_core.messages import SystemMessage

def create_orchestrator_node(llm_with_tools):
    """Create the main orchestrator node"""
    
    # Simple but intelligent system prompt
    SYSTEM_PROMPT = """You are a V2 orchestrator that executes agents using tools. 

🔧 AVAILABLE TOOLS:
- execute_math_agent: For math/arithmetic questions
- execute_weather_agent: For weather questions
- execute_slack_agent: For sending messages to Slack channels
- execute_google_meet_agent: For scheduling Google Meet meetings and calendar operations

🎯 YOUR JOB:
1. Analyze the user's question
2. Use the appropriate tool to execute the right agent
3. For complex questions, you can use multiple tools in sequence
4. Pass context between tools when needed

EXAMPLES:
- "Add 5 and 10" → Use execute_math_agent
- "Weather in London?" → Use execute_weather_agent  
- "Send 'Hello team' to general channel" → Use execute_slack_agent
- "Schedule a team meeting for tomorrow at 2 PM" → Use execute_google_meet_agent
- "Create a Google Meet call for Friday at 10 AM" → Use execute_google_meet_agent

Be smart about using tools and passing context!"""

    def orchestrator_with_tools(state):
        """Main orchestrator node with tool capabilities"""
        messages = state["messages"].copy()
        
        # Add system prompt
        has_system = any(getattr(msg, 'type', None) == 'system' for msg in messages)
        if not has_system:
            system_msg = SystemMessage(content=SYSTEM_PROMPT)
            messages = [system_msg] + messages
        
        # Add context from previous agent results if available
        if state.get("context"):
            context_info = f"\nPrevious context: {state['context']}"
            if messages and hasattr(messages[-1], 'content'):
                messages[-1].content += context_info
        
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}
    
    return orchestrator_with_tools 