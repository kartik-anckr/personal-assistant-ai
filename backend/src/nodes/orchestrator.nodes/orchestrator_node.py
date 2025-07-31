"""
Simplified Orchestrator Node - LLM-driven agent selection for two-agent architecture
Focuses on Slack and Weather agents with intelligent routing
"""

from langchain_core.messages import SystemMessage, ToolMessage

def create_orchestrator_node(llm_with_tools, base_llm=None):
    """Create the orchestrator node for routing and response formatting"""
    
    # Use provided base LLM or fallback to the one with tools
    if base_llm is None:
        base_llm = llm_with_tools
    
    # Enhanced system prompt for three-agent selection
    ENHANCED_SYSTEM_PROMPT = """Hey there! I'm your friendly personal assistant with three amazing specialist friends! 😊

🤖 MY SPECIALIST FRIENDS:
- invoke_slack_agent: Your Slack messenger for team communication
- invoke_weather_agent: Your weather expert for forecasts and climate data
- invoke_calendar_agent: Your calendar assistant for scheduling events and meetings

💫 HOW I HELP YOU:
I listen to what you need and automatically connect you with the right specialist!

🎯 EXAMPLES:
📱 SLACK: "Send hello to team channel" → Slack specialist handles it!
🌤️ WEATHER: "Weather in London?" → Weather expert provides forecast!
📅 CALENDAR: "Schedule meeting tomorrow at 2pm" → Calendar assistant creates the event!

Just tell me what you need naturally - I'll route you to the perfect helper! 🚀"""

    def simplified_orchestrator_with_tools(state):
        """Orchestrator node that handles both routing and response formatting"""
        messages = state["messages"].copy()
        
        # Check if we have tool results (coming back from manager)
        has_tool_results = any(getattr(msg, 'type', None) == 'tool' for msg in messages)
        
        if has_tool_results:
            # We're formatting the final response based on tool results
            RESPONSE_FORMATTING_PROMPT = """You just received results from your specialist friends! Now create a warm, friendly, personalized response for the user.

🎯 YOUR JOB NOW:
- Take the raw data/results from your specialist friends
- Transform it into a conversational, helpful response
- Add personality and warmth to make it feel like talking to a buddy
- Keep it natural and engaging

💬 RESPONSE STYLE:
- Start with something friendly like "Here's what I found out for you!" or "Great question!"
- Present the information in a conversational way
- Add helpful context or suggestions when appropriate
- End with something encouraging or offer further help

Remember: You're not just relaying data - you're being a helpful, friendly assistant who cares about giving a great experience!"""
            
            # Add the response formatting prompt
            system_msg = SystemMessage(content=RESPONSE_FORMATTING_PROMPT)
            messages = [system_msg] + messages
            
            # Use base LLM to generate final response (no tools)
            response = base_llm.invoke(messages)
            print(f"🎭 [ORCHESTRATOR] Generating friendly response based on tool results")
            
        else:
            # Initial user request - route to appropriate tools
            has_system = any(getattr(msg, 'type', None) == 'system' for msg in messages)
            if not has_system:
                system_msg = SystemMessage(content=ENHANCED_SYSTEM_PROMPT)
                messages = [system_msg] + messages
            
            # Add context from previous agent results if available
            if state.get("context"):
                context_info = f"\nPrevious context: {state['context']}"
                if messages and hasattr(messages[-1], 'content'):
                    messages[-1].content += context_info
            
            response = llm_with_tools.invoke(messages)
            
            # Ensure user_id is passed to tool calls
            user_id = state.get("user_id")
            if hasattr(response, 'tool_calls') and response.tool_calls and user_id:
                for tool_call in response.tool_calls:
                    if 'args' in tool_call and isinstance(tool_call['args'], dict):
                        tool_call['args']['user_id'] = user_id
                        print(f"🎭 [ORCHESTRATOR] Added user_id to tool call: {user_id}")
            
            print(f"🎭 [ORCHESTRATOR] Routing user request to appropriate specialist")
        
        # Preserve user_id in the state
        return {"messages": [response], "user_id": state.get("user_id")}
    
    return simplified_orchestrator_with_tools

# Keep backward compatibility with original function name
def create_simplified_orchestrator_node(llm_with_tools, base_llm=None):
    """Create simplified orchestrator node - new enhanced version"""
    return create_orchestrator_node(llm_with_tools, base_llm) 