"""
Enhanced Slack Chatbot Node - Handles comprehensive Slack operations
Uses multiple Slack tools with LLM-driven tool selection
"""

from langchain_core.messages import SystemMessage

def create_slack_chatbot_node(llm_with_tools, available_channels):
    """Create the enhanced slack chatbot node"""
    
    # Enhanced system prompt for multiple Slack capabilities
    ENHANCED_SLACK_PROMPT = f"""You are an enhanced Slack specialist agent with comprehensive Slack capabilities.

📱 YOUR ROLE:
- You handle ALL Slack-related requests including messaging, reading, and channel management
- You have access to multiple Slack tools for different types of requests
- Choose the most appropriate tool based on the user's specific needs
- Provide helpful, accurate Slack assistance

🔧 AVAILABLE TOOLS:
- send_slack_message: Send messages to Slack channels
- read_slack_messages: Read recent messages from channels
- list_slack_channels: List all available channels
- get_channel_info: Get detailed information about specific channels

📋 AVAILABLE CHANNELS: {available_channels}

🎯 EXAMPLES:
- "Send 'Hello team' to development channel" → Use send_slack_message
- "What are the latest messages in team channel?" → Use read_slack_messages
- "Show me all available channels" → Use list_slack_channels
- "Get info about the development channel" → Use get_channel_info
- "Send a message to team and then read recent messages" → Use both send_slack_message and read_slack_messages

Be intelligent about tool selection and provide helpful Slack assistance."""

    def enhanced_slack_chatbot(state):
        """Enhanced slack chatbot node function"""
        messages = state["messages"].copy()
        
        # Add enhanced Slack system prompt
        has_system = any(getattr(msg, 'type', None) == 'system' for msg in messages)
        if not has_system:
            system_msg = SystemMessage(content=ENHANCED_SLACK_PROMPT)
            messages = [system_msg] + messages
            
        return {"messages": [llm_with_tools.invoke(messages)]}
    
    return enhanced_slack_chatbot

# Keep backward compatibility
def create_enhanced_slack_chatbot_node(llm_with_tools, available_channels):
    """Create enhanced slack chatbot node - new enhanced version"""
    return create_slack_chatbot_node(llm_with_tools, available_channels) 