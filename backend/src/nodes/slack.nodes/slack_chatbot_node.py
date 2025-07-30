"""
Simplified Slack Chatbot Node - Handles Slack messaging
Uses direct tool binding for send message functionality
"""

from langchain_core.messages import SystemMessage, ToolMessage
import sys
import os

# Import slack tools for execution
_slack_tools_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'slack.tools')
sys.path.insert(0, _slack_tools_dir)
try:
    from slack_messaging import send_slack_message
finally:
    sys.path.remove(_slack_tools_dir)

def create_slack_chatbot_node(llm_with_tools, available_channels):
    """Create the simplified slack chatbot node with direct tool execution"""
    
    # Friendly Slack assistant system prompt with tool information
    ENHANCED_SLACK_PROMPT = f"""Hey there! I'm your Slack buddy, and I'm here to help you send messages to your team! 💬

Think of me as your personal Slack messenger who can quickly send messages to any channel in your workspace. Just tell me what you want to say and which channel, and I'll send it right away!

Here's how I can help you:

✉️ **Send messages**: Just tell me what you want to say and which channel, and I'll send it instantly! No need to switch tabs or navigate anywhere.

🔧 **My tool**: 
- send_slack_message: I use this to send messages to Slack channels

📋 **Available channels in your workspace**: {available_channels}

🎯 **Examples of how I work**:
- "Send hello to team channel" → I'll use send_slack_message
- "Tell the development channel I'll be late" → I'll use send_slack_message  
- "Send a message to team saying meeting is cancelled" → I'll use send_slack_message

I'm pretty good at understanding what you need - just talk to me naturally! Say things like "send hello to the team channel" or "tell the development channel I'll be late" and I'll know exactly what to do.

Ready to help you communicate with your team? What message would you like me to send? 🚀"""

    # Create a mapping of tool names to actual functions
    tool_map = {
        'send_slack_message': send_slack_message
    }

    def enhanced_slack_chatbot(state):
        """Slack chatbot node function with proper tool execution"""
        messages = state["messages"].copy()
        
        # Add Slack system prompt
        has_system = any(getattr(msg, 'type', None) == 'system' for msg in messages)
        if not has_system:
            system_msg = SystemMessage(content=ENHANCED_SLACK_PROMPT)
            messages = [system_msg] + messages
        
        # Get LLM response (may include tool calls)
        response = llm_with_tools.invoke(messages)
        
        # Check if the response contains tool calls
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"🔧 Slack agent executing {len(response.tool_calls)} tool(s)")
            
            # Add the LLM's response with tool calls to messages
            messages.append(response)
            
            # Execute each tool call
            for tool_call in response.tool_calls:
                tool_name = tool_call['name']
                tool_args = tool_call['args']
                tool_id = tool_call['id']
                
                print(f"📱 Executing tool: {tool_name} with args: {tool_args}")
                
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
            return {"messages": [final_response]}
        else:
            # No tool calls, return the response directly
            return {"messages": [response]}
    
    return enhanced_slack_chatbot

# Keep backward compatibility
def create_enhanced_slack_chatbot_node(llm_with_tools, available_channels):
    """Create simplified slack chatbot node - simplified version with direct tool execution"""
    return create_slack_chatbot_node(llm_with_tools, available_channels) 