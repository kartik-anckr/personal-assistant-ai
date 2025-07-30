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
    
    # Enhanced system prompt for two-agent selection
    SIMPLIFIED_SYSTEM_PROMPT = """Hey there! I'm your friendly personal assistant and I'm here to help you with anything you need! 😊

Think of me as your helpful buddy who knows exactly who to connect you with for different tasks. I've got two amazing specialist friends who are experts in their areas:

🤖 MY SPECIALIST FRIENDS:
- invoke_slack_agent: Your Slack messenger who sends messages to Slack channels quickly and easily
- invoke_weather_agent: Your weather expert who knows everything about forecasts, climate data, and weather conditions

💫 HOW I HELP YOU:
I listen to what you need and automatically connect you with the right specialist friend! No need for special keywords - just talk to me naturally like you would to any friend.

🎯 HERE'S HOW IT WORKS:
- "Send hello to team channel" → I'll get your Slack messenger to help!
- "Tell the development channel I'll be late" → Your Slack friend will send that message!
- "Send a message to the team saying meeting is cancelled" → Perfect job for your Slack specialist!
- "Weather in London?" → Time to call your weather expert!
- "Give me a 5-day forecast for Tokyo" → Your weather buddy will sort this out!
- "Compare weather between NYC and LA" → Weather specialist to the rescue!

Just tell me what you need in your own words, and I'll make sure you get connected with exactly the right helper. I'm here to make your life easier! 🚀"""

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
                system_msg = SystemMessage(content=SIMPLIFIED_SYSTEM_PROMPT)
                messages = [system_msg] + messages
            
            # Add context from previous agent results if available
            if state.get("context"):
                context_info = f"\nPrevious context: {state['context']}"
                if messages and hasattr(messages[-1], 'content'):
                    messages[-1].content += context_info
            
            response = llm_with_tools.invoke(messages)
            print(f"🎭 [ORCHESTRATOR] Routing user request to appropriate specialist")
        
        return {"messages": [response]}
    
    return simplified_orchestrator_with_tools

# Keep backward compatibility with original function name
def create_simplified_orchestrator_node(llm_with_tools, base_llm=None):
    """Create simplified orchestrator node - new enhanced version"""
    return create_orchestrator_node(llm_with_tools, base_llm) 