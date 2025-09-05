import os
from dotenv import load_dotenv

load_dotenv()

# Time-based monitoring configuration
MONITORING_START_HOUR = 18  # 6 PM
MONITORING_END_HOUR = 9     # 9 AM
TIMEZONE = "America/New_York"  # EST/EDT

# Slack configuration
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "https://hooks.slack.com/services/XXXX/YYYY/ZZZZ")

# Flask configuration for local server
FLASK_ENV = os.getenv("FLASK_ENV", "production")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
HOST = os.getenv("HOST", "0.0.0.0")  # Allow external connections
PORT = int(os.getenv("PORT", 5000))  # Use PORT env var for Render compatibility
