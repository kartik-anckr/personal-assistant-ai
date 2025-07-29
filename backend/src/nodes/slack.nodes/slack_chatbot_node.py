"""
Slack Chatbot Node - Main slack agent node with tool capabilities
"""

from langchain_core.messages import SystemMessage

def create_slack_chatbot_node(llm_with_tools, available_channels):
    """Create the slack chatbot node"""
    
    # Slack-specific system prompt
    SLACK_PROMPT = f"""You are a specialized Slack messaging agent. Your expertise is sending messages to Slack channels.

📱 YOUR ROLE:
- You ONLY handle Slack messaging requests
- Use send_slack_message tool to send messages to authorized channels
- Always validate channel permissions before sending
- Provide clear feedback on message delivery status

📋 AVAILABLE CHANNELS: {available_channels}

🎯 EXAMPLES:
- "Send 'Hello team' to general" → Use send_slack_message tool with channel='general'
- "Post update to development channel" → Use send_slack_message tool with channel='development'
- "Send message to random-channel" → Will return permission error

⚠️ IMPORTANT:
- Only send messages to authorized channels: {available_channels}
- For unauthorized channels, inform user about permission restrictions
- Always confirm successful message delivery"""

    def slack_chatbot(state):
        messages = state["messages"].copy()
        
        # Add Slack system prompt
        has_system = any(getattr(msg, 'type', None) == 'system' for msg in messages)
        if not has_system:
            system_msg = SystemMessage(content=SLACK_PROMPT)
            messages = [system_msg] + messages
            
        return {"messages": [llm_with_tools.invoke(messages)]}
    
    return slack_chatbot 