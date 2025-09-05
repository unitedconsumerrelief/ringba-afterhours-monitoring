import datetime
import json
import logging
import pytz
from flask import Flask, request, jsonify
from slack_notify import send_slack_alert
from config import MONITORING_START_HOUR, MONITORING_END_HOUR, TIMEZONE, FLASK_DEBUG, HOST, PORT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ringba_webhook.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)

def has_valid_target(target_name):
    """Check if target name is valid (not blank, empty, or 'No value' variations)"""
    if not target_name:
        return False
    
    # Convert to string and strip whitespace
    target_str = str(target_name).strip()
    
    # Check if empty after stripping
    if not target_str:
        return False
    
    # Check for "No value" variations (case insensitive)
    no_value_variations = [
        "no value", "-no value-", "no_value", "no-value",
        "none", "null", "empty", "blank"
    ]
    
    if target_str.lower() in no_value_variations:
        return False
    
    return True

def is_within_monitoring_hours(timestamp=None):
    """Check if Ringba's timestamp is within 6pm EST - 9am EST"""
    try:
        if timestamp:
            # Parse Ringba's timestamp (already in EST)
            if isinstance(timestamp, str):
                # Try different timestamp formats
                for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%SZ"]:
                    try:
                        dt = datetime.datetime.strptime(timestamp, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    # If no format matches, use current time
                    dt = datetime.datetime.now()
            else:
                dt = timestamp
        else:
            # No timestamp provided, use current time
            dt = datetime.datetime.now()
        
        # Get hour from the timestamp (already in EST)
        current_hour = dt.hour
        
        # Check if within monitoring hours (6pm to 9am next day)
        # 6pm = 18, 9am = 9
        if current_hour >= MONITORING_START_HOUR or current_hour < MONITORING_END_HOUR:
            return True
        
        return False
        
    except Exception as e:
        logging.error(f"Error checking monitoring hours: {str(e)}")
        return False

def passes_filter(target_name, timestamp=None):
    """New filter logic:
    1. Check if within time range (6pm EST - 9am EST) using Ringba's timestamp
    2. Check if target name is valid (not blank/empty/No value)
    3. Monitor ALL calls (no campaign filtering needed)
    """
    # Check if within monitoring hours using Ringba's timestamp
    if not is_within_monitoring_hours(timestamp):
        logging.info(f"Call outside monitoring hours (6pm EST - 9am EST) - Ringba timestamp: {timestamp}")
        return False
    
    # Check if target name is valid
    if not has_valid_target(target_name):
        logging.info(f"Call filtered out - invalid target name: '{target_name}'")
        return False
    
    return True

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Ringba After Hours Monitor",
        "monitoring_hours": f"{MONITORING_START_HOUR}:00 - {MONITORING_END_HOUR}:00 EST/EDT",
        "timezone": TIMEZONE
    }), 200

@app.route("/ringba-webhook", methods=["POST"])
def ringba_webhook():
    try:
        # Handle Slack URL verification challenge
        data = request.get_json()
        if data and data.get("type") == "url_verification":
            challenge = data.get("challenge")
            if challenge:
                return jsonify({"challenge": challenge}), 200
        
        # Log all request details
        content_type = request.headers.get('Content-Type', '')
        content_length = request.headers.get('Content-Length', '0')
        user_agent = request.headers.get('User-Agent', '')
        
        logging.info(f"=== NEW WEBHOOK REQUEST ===")
        logging.info(f"Content-Type: '{content_type}'")
        logging.info(f"Content-Length: '{content_length}'")
        logging.info(f"User-Agent: '{user_agent}'")
        logging.info(f"Request Headers: {dict(request.headers)}")
        
        # Check if request has any data
        raw_data = request.data
        logging.info(f"Raw data length: {len(raw_data)} bytes")
        
        if len(raw_data) == 0:
            logging.warning("Request has no data - empty body. This might be a Ringba configuration issue.")
            return jsonify({
                "status": "received",
                "message": "Empty request received - check Ringba webhook configuration",
                "expected_format": {
                    "targetName": "actual target name (not blank/empty/No value)",
                    "callerId": "example_caller_id",
                    "timestamp": "2024-01-01T12:00:00Z"
                }
            }), 200
        
        # Try to decode and log the raw data
        try:
            raw_text = raw_data.decode('utf-8')
            logging.info(f"Raw data: '{raw_text}'")
        except Exception as e:
            logging.error(f"Could not decode raw data: {str(e)}")
            return jsonify({"error": "Invalid request encoding"}), 400
        
        # Try to parse JSON
        data = None
        if 'application/json' in content_type:
            data = request.get_json()
        else:
            try:
                data = request.get_json(force=True)
            except:
                try:
                    data = json.loads(raw_text)
                except Exception as e:
                    logging.error(f"Could not parse JSON. Raw text: '{raw_text}', Error: {str(e)}")
                    return jsonify({"error": "Invalid JSON data"}), 400
        
        if not data:
            logging.error("No JSON data received")
            return jsonify({"error": "No JSON data received"}), 400
        
        # Extract call data
        target_name = data.get("targetName", "")
        caller_id = data.get("callerId", "Unknown")
        timestamp = data.get("timestamp") or data.get("callTime") or data.get("callDate")
        
        logging.info(f"Parsed data: targetName='{target_name}', callerId='{caller_id}', timestamp='{timestamp}'")
        
        # Check if this call matches our filter
        if not passes_filter(target_name, timestamp):
            logging.info(f"Call filtered out: targetName='{target_name}', timestamp='{timestamp}'")
            return jsonify({"status": "filtered", "message": "Call does not match filter criteria"}), 200
        
        # Process the call - use Ringba's timestamp (already in EST)
        if timestamp:
            time_of_call = timestamp
        else:
            # No timestamp provided, use current time
            utc_time = datetime.datetime.now(datetime.UTC)
            eastern_tz = pytz.timezone(TIMEZONE)
            eastern_time = utc_time.astimezone(eastern_tz)
            time_of_call = eastern_time.strftime("%Y-%m-%d %I:%M:%S %p %Z")
        
        # Send Slack notification
        slack_success = send_slack_alert(caller_id, time_of_call, target_name, "After Hours Call")
        if not slack_success:
            logging.error("Failed to send Slack notification")
            return jsonify({"error": "Failed to send Slack notification"}), 500
        
        logging.info(f"Successfully processed after hours call from {caller_id} with target {target_name}")
        
        return jsonify({
            "caller_id": caller_id,
            "target_name": target_name,
            "status": "success",
            "time": time_of_call,
            "message": "After hours call notification sent"
        }), 200
        
    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    logging.info(f"Starting Ringba After Hours Monitor on {HOST}:{PORT}")
    logging.info(f"Monitoring hours: {MONITORING_START_HOUR}:00 - {MONITORING_END_HOUR}:00 {TIMEZONE}")
    app.run(
        host=HOST,
        port=PORT,
        debug=FLASK_DEBUG
    )