"""
Calendar Chatbot Node - Handles calendar-related conversations with direct tool execution
"""

from langchain_core.messages import SystemMessage, ToolMessage
import sys
import os

# Import calendar tools for direct execution
_calendar_tools_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'calendar.tools')
sys.path.insert(0, _calendar_tools_dir)
try:
    from calendar_tools import create_calendar_event
finally:
    sys.path.remove(_calendar_tools_dir)

def create_calendar_chatbot_node(llm_with_tools):
    """Create calendar chatbot node with direct tool execution capabilities"""

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

    # Create a mapping of tool names to actual functions
    tool_map = {
        'create_calendar_event': create_calendar_event
    }

    def calendar_chatbot(state):
        """Calendar chatbot node function with direct tool execution"""
        messages = state["messages"].copy()
        user_id = state.get("user_id", "unknown")
        
        print(f"📅 [CALENDAR CHATBOT] Processing with user_id: {user_id}")

        # Add system prompt
        has_system = any(getattr(msg, 'type', None) == 'system' for msg in messages)
        if not has_system:
            system_msg = SystemMessage(content=CALENDAR_PROMPT)
            messages = [system_msg] + messages

        # Get LLM response (may include tool calls)
        response = llm_with_tools.invoke(messages)

        print(f"📅 [CALENDAR CHATBOT] Response: {response}")
        print(f"📅 [CALENDAR CHATBOT] Tool calls: {response.tool_calls}")

        # Check if the response contains tool calls
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"🔧 Calendar agent executing {len(response.tool_calls)} tool(s)")
            
            # Add the LLM's response with tool calls to messages
            messages.append(response)
            
            # Execute each tool call
            for tool_call in response.tool_calls:
                tool_name = tool_call['name']
                tool_args = tool_call['args']
                tool_id = tool_call['id']
                
                # Ensure user_id is passed to calendar tools
                tool_args['user_id'] = user_id
                
                print(f"📅 Executing tool: {tool_name} with args: {tool_args}")
                
                try:
                    # Execute the tool
                    if tool_name in tool_map:
                        tool_result = tool_map[tool_name].invoke(tool_args)
                        print(f"✅ Tool {tool_name} result: {tool_result}")
                    else:
                        tool_result = f"Error: Unknown tool {tool_name}"
                        print(f"❌ Unknown tool: {tool_name}")
                    
                    # Add tool result as a ToolMessage
                    tool_message = ToolMessage(
                        content=str(tool_result),
                        tool_call_id=tool_id,
                        name=tool_name
                    )
                    messages.append(tool_message)
                    
                except Exception as e:
                    error_msg = f"Error executing {tool_name}: {str(e)}"
                    print(f"❌ {error_msg}")
                    tool_message = ToolMessage(
                        content=error_msg,
                        tool_call_id=tool_id,
                        name=tool_name
                    )
                    messages.append(tool_message)
            
            # Get final response from LLM with tool results
            final_response = llm_with_tools.invoke(messages)
            return {"messages": [final_response], "user_id": user_id}
        else:
            # No tool calls, return the response directly
            return {"messages": [response], "user_id": user_id}

    return calendar_chatbot 