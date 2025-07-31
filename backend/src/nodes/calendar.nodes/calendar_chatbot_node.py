"""
Calendar Chatbot Node - Handles calendar-related conversations
"""

from langchain_core.messages import SystemMessage

def create_calendar_chatbot_node(llm_with_tools):
    """Create calendar chatbot node with event creation capabilities"""

    CALENDAR_PROMPT = """You are a helpful Google Calendar assistant that specializes in creating calendar events.

🗓️ YOUR ROLE:
- Help users create calendar events from natural language descriptions
- Parse event details like title, date, time, and duration from user input
- Use the create_calendar_event tool to actually create events
- Provide clear feedback about created events

🔧 AVAILABLE TOOLS:
- create_calendar_event: Creates calendar events from natural language prompts

🎯 EXAMPLES:
- "Schedule meeting tomorrow at 2pm" → Extract: meeting, tomorrow, 2pm
- "Plan dentist appointment next Friday 10am" → Extract: dentist appointment, next Friday, 10am
- "Add team standup every Monday 9am" → Extract: team standup, Monday, 9am
- "Book lunch with client Thursday 12:30pm" → Extract: lunch with client, Thursday, 12:30pm

📝 RESPONSE FORMAT:
When creating events, always:
1. Acknowledge what event you're creating
2. Show the parsed details (title, date, time)
3. Use the tool to create the event
4. Confirm success or explain any issues

Be conversational and helpful - users should feel like they're talking to a personal assistant!"""

    def calendar_chatbot(state):
        """Calendar chatbot node function"""
        messages = state["messages"]
        user_id = state.get("user_id", "unknown")
        
        print(f"📅 [CALENDAR NODE] Processing with user_id: {user_id}")

        # Add system prompt with user context
        system_message = SystemMessage(content=CALENDAR_PROMPT)
        messages_with_system = [system_message] + messages

        # Get LLM response
        response = llm_with_tools.invoke(messages_with_system)

        # If the response has tool calls, update them with the user_id
        if hasattr(response, 'tool_calls') and response.tool_calls:
            for tool_call in response.tool_calls:
                if 'args' in tool_call and isinstance(tool_call['args'], dict):
                    # Ensure user_id is passed to calendar tools
                    tool_call['args']['user_id'] = user_id
                    print(f"📅 [CALENDAR NODE] Updated tool call with user_id: {user_id}")

        # If the response has tool calls, they'll be handled by the ToolNode
        return {"messages": [response], "user_id": user_id}

    return calendar_chatbot 