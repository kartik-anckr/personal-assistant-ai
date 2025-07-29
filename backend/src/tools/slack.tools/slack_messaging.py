"""
Enhanced Slack tools for comprehensive Slack operations
Includes messaging, reading, channel management, and information tools
"""

import os
import json
import requests
from langchain_core.tools import tool

# Predefined Slack channels with their webhook URLs
SLACK_CHANNELS = {
    "team": "https://hooks.slack.com/services/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",
    "development": "https://hooks.slack.com/services/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", 
}

@tool
def send_slack_message(channel: str, message: str) -> str:
    """
    Send a message to a Slack channel via webhook
    
    Args:
        channel: The Slack channel name (e.g., 'team', 'development')
        message: The message to send
    
    Returns:
        Success/failure message
    """
    print(f"🔔 [SLACK TOOL] Attempting to send message to #{channel}")
    
    # Check if channel exists in our allowed channels
    if channel not in SLACK_CHANNELS:
        available_channels = ", ".join(SLACK_CHANNELS.keys())
        error_msg = f"❌ I don't have permission to send messages to #{channel}. Available channels: {available_channels}"
        print(f"🔔 [SLACK TOOL] {error_msg}")
        return error_msg
    
    # Get webhook URL for the channel
    webhook_url = SLACK_CHANNELS[channel]
    
    # Prepare Slack message payload
    payload = {
        "text": message,
        "channel": f"#{channel}",
        "username": "Assistant Bot",
        "icon_emoji": ":robot_face:"
    }
    
    try:
        # Send POST request to Slack webhook
        response = requests.post(
            webhook_url,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'},
            timeout=10
        )

        print("webhook_url", webhook_url)
        print(f"🔔 [SLACK TOOL] Response: {response.text}")
        
        if response.status_code == 200:
            success_msg = f"✅ Message sent successfully to #{channel}"
            print(f"🔔 [SLACK TOOL] {success_msg}")
            return success_msg
        else:
            error_msg = f"❌ Failed to send message to #{channel}. Status code: {response.status_code}"
            print(f"🔔 [SLACK TOOL] {error_msg}")
            return error_msg
            
    except requests.exceptions.RequestException as e:
        error_msg = f"❌ Network error sending message to #{channel}: {str(e)}"
        print(f"🔔 [SLACK TOOL] {error_msg}")
        return error_msg
    except Exception as e:
        error_msg = f"❌ Unexpected error sending message to #{channel}: {str(e)}"
        print(f"🔔 [SLACK TOOL] {error_msg}")
        return error_msg

@tool
def read_slack_messages(channel: str, limit: int = 10) -> str:
    """
    Read recent messages from a Slack channel (simulated)
    
    Args:
        channel: The Slack channel name to read from
        limit: Number of recent messages to retrieve (default 10)
    
    Returns:
        Recent messages from the channel
    """
    print(f"📖 [SLACK TOOL] Reading messages from #{channel}")
    
    # Check if channel exists
    if channel not in SLACK_CHANNELS:
        available_channels = ", ".join(SLACK_CHANNELS.keys())
        error_msg = f"❌ Channel #{channel} not available. Available channels: {available_channels}"
        print(f"📖 [SLACK TOOL] {error_msg}")
        return error_msg
    
    # Simulated message data (in real app, would use Slack API to read messages)
    mock_messages = {
        "team": [
            "🎯 [Alice] Great work on the project launch!",
            "🔧 [Bob] Deployed the new features to production",
            "📊 [Carol] Updated the team dashboard",
            "🎉 [David] Celebrating our milestone!",
            "💡 [Eve] Had a great idea for the next sprint"
        ],
        "development": [
            "🐛 [Alice] Fixed the bug in user authentication",
            "⚡ [Bob] Optimized database queries - 50% faster!",
            "🔍 [Carol] Code review completed for PR #123",
            "🚀 [David] New deployment pipeline is ready",
            "📝 [Eve] Updated API documentation"
        ]
    }
    
    channel_messages = mock_messages.get(channel, ["No recent messages"])
    limited_messages = channel_messages[:min(limit, len(channel_messages))]
    
    result = f"📖 Recent messages from #{channel}:\n" + "\n".join(limited_messages)
    print(f"📖 [SLACK TOOL] Retrieved {len(limited_messages)} messages")
    return result

@tool
def list_slack_channels() -> str:
    """
    List all available Slack channels that the bot can access
    
    Returns:
        List of available channels
    """
    print(f"📋 [SLACK TOOL] Listing available channels")
    
    channels_info = []
    for channel, webhook in SLACK_CHANNELS.items():
        # Provide basic channel info
        if channel == "team":
            description = "General team discussions and announcements"
        elif channel == "development":
            description = "Development updates, code reviews, and technical discussions"
        else:
            description = "General purpose channel"
            
        channels_info.append(f"#{channel} - {description}")
    
    result = f"📋 Available Slack channels:\n" + "\n".join(channels_info)
    print(f"📋 [SLACK TOOL] Listed {len(SLACK_CHANNELS)} channels")
    return result

@tool
def get_channel_info(channel: str) -> str:
    """
    Get detailed information about a specific Slack channel
    
    Args:
        channel: The Slack channel name to get info about
    
    Returns:
        Detailed channel information
    """
    print(f"ℹ️ [SLACK TOOL] Getting info for #{channel}")
    
    # Check if channel exists
    if channel not in SLACK_CHANNELS:
        available_channels = ", ".join(SLACK_CHANNELS.keys())
        error_msg = f"❌ Channel #{channel} not found. Available channels: {available_channels}"
        print(f"ℹ️ [SLACK TOOL] {error_msg}")
        return error_msg
    
    # Simulated channel info (in real app, would use Slack API)
    channel_info = {
        "team": {
            "name": "team",
            "description": "General team discussions and announcements",
            "members": 15,
            "purpose": "Team coordination and general communication",
            "created": "2024-01-15",
            "topic": "Weekly team updates and important announcements"
        },
        "development": {
            "name": "development", 
            "description": "Development updates, code reviews, and technical discussions",
            "members": 8,
            "purpose": "Technical discussions and development coordination",
            "created": "2024-01-20",
            "topic": "Code reviews, deployments, and technical updates"
        }
    }
    
    info = channel_info.get(channel, {})
    
    result = f"""ℹ️ Channel #{channel} Information:
📝 Description: {info.get('description', 'No description')}
👥 Members: {info.get('members', 'Unknown')}
🎯 Purpose: {info.get('purpose', 'General purpose')}
📅 Created: {info.get('created', 'Unknown')}
💬 Topic: {info.get('topic', 'No topic set')}"""
    
    print(f"ℹ️ [SLACK TOOL] Retrieved info for #{channel}")
    return result 