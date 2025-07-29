"""
Slack messaging tool for sending messages to Slack channels via webhooks
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
        channel: The Slack channel name (e.g., 'general', 'development')
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