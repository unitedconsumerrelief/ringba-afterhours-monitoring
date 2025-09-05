import logging
from flask import Flask, request, jsonify
from datetime import datetime
from config import RINGBA_FILTERS, GOOGLE_SHEET_ID, FLASK_DEBUG
from google_sheets import append_row_to_sheet
from slack_notify import send_slack_alert

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ringba_webhook_port8080.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)

def passes_filter(data):
    campaign_name = data.get("campaignName", "")
    target_name = data.get("targetName", "")
    
    return (campaign_name == RINGBA_FILTERS["campaign_name"] and 
            target_name == RINGBA_FILTERS["target_name"])

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Ringba Webhook Handler (Port 8080)",
        "filters": RINGBA_FILTERS,
        "server": "local"
    }), 200

@app.route("/ringba-webhook", methods=["POST"])
def ringba_webhook():
    try:
        data = request.json
        if not data:
            logging.warning("No JSON data received in webhook")
            return jsonify({"error": "No JSON received"}), 400

        logging.info(f"Received webhook: campaignName={data.get('campaignName')}, targetName={data.get('targetName')}")

        if not passes_filter(data):
            logging.info("Webhook filtered out - doesn't match criteria")
            return jsonify({"status": "ignored", "reason": "filtered"}), 200

        caller_id = data.get("callerId", "Unknown")
        time_of_call = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        sheet_success = append_row_to_sheet(time_of_call, caller_id)
        if not sheet_success:
            logging.error("Failed to append to Google Sheet")
            return jsonify({"error": "Failed to update Google Sheet"}), 500

        sheet_link = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}"
        slack_success = send_slack_alert(caller_id, time_of_call, sheet_link)
        
        if not slack_success:
            logging.warning("Failed to send Slack notification")

        logging.info(f"Successfully processed call from {caller_id}")
        return jsonify({
            "status": "success",
            "caller_id": caller_id,
            "time": time_of_call
        }), 200

    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    logging.info("Starting Ringba Webhook Handler on 0.0.0.0:8080")
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=False
    )

