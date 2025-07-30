"""
Simplified Slack tools module - only message sending
"""

from .slack_messaging import (
    send_slack_message,
    SLACK_CHANNELS
)

__all__ = [
    'send_slack_message',
    'SLACK_CHANNELS'
] 