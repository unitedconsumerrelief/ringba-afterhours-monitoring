import requests
from config import SLACK_WEBHOOK_URL
import logging

def send_slack_alert(caller_id, time_of_call, target_name, call_type="After Hours Call"):
    try:
        # Determine emoji and styling based on call type
        emoji = "🌙"
        call_type_text = f"*{call_type}*"
        
        message = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{emoji} *{call_type_text}*\n\n• *Caller ID:* `{caller_id}`\n• *Time:* `{time_of_call}`\n• *Target:* `{target_name}`\n• *Status:* `Active Monitoring`"
                    }
                }
            ]
        }
        
        response = requests.post(SLACK_WEBHOOK_URL, json=message, timeout=10)
        response.raise_for_status()
        
        logging.info(f"Successfully sent Slack notification for {call_type.lower()} from caller {caller_id}")
        return True
        
    except Exception as e:
        logging.error(f"Error sending Slack notification: {str(e)}")
        return False
