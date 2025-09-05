# Ringba Webhook Handler

A Python Flask application that receives real-time call data from Ringba via webhooks, filters calls by campaign and target names, logs them to Google Sheets, and sends notifications to Slack.

## Features

- ✅ Real-time webhook processing from Ringba
- ✅ Call filtering by campaignName and targetName
- ✅ Automatic logging to Google Sheets with headers
- ✅ Slack notifications with rich formatting
- ✅ Health check endpoint
- ✅ Comprehensive error handling and logging
- ✅ Environment-based configuration
- ✅ Ready for deployment to cloud platforms

## File Structure

```
Ringba_NoValues_Report/
├── main.py                 # Flask application and webhook handler
├── config.py              # Configuration management
├── google_sheets.py       # Google Sheets integration
├── slack_notify.py        # Slack notification service
├── requirements.txt       # Python dependencies
├── Procfile              # Deployment configuration
├── runtime.txt           # Python version specification
├── test_webhook.py       # Test script for webhooks
├── env.example           # Environment variables template
└── README.md             # This file
```

## Setup Instructions

### 1. Prerequisites

Before setting up the application, you'll need:

#### Google Sheets Setup
1. **Create a Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable the Google Sheets API

2. **Create Service Account**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Download the JSON key file as `credentials.json`
   - Place it in your project root

3. **Create Google Sheet**:
   - Create a new Google Sheet
   - Share it with your service account email (found in credentials.json)
   - Copy the Sheet ID from the URL

#### Slack Setup
1. **Create Slack App**:
   - Go to [Slack API](https://api.slack.com/apps)
   - Click "Create New App" > "From scratch"
   - Choose your workspace

2. **Enable Incoming Webhooks**:
   - Go to "Features" > "Incoming Webhooks"
   - Click "Activate Incoming Webhooks"
   - Click "Add New Webhook to Workspace"
   - Choose a channel and copy the webhook URL

### 2. Local Development Setup

1. **Clone and Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**:
   ```bash
   # Copy the example file
   cp env.example .env
   
   # Edit .env with your actual values
   nano .env
   ```

3. **Update Configuration**:
   - Set your actual campaign and target names
   - Add your Google Sheet ID
   - Add your Slack webhook URL

4. **Run the Application**:
   ```bash
   python main.py
   ```

### 3. Testing Locally

#### Using ngrok (Recommended)
1. **Install ngrok**:
   ```bash
   # Download from https://ngrok.com/download
   # Or use: npm install -g ngrok
   ```

2. **Start ngrok**:
   ```bash
   ngrok http 5000
   ```

3. **Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)

4. **Test with the provided script**:
   ```bash
   # Update test_webhook.py with your ngrok URL
   python test_webhook.py
   ```

#### Using curl
```bash
curl -X POST http://localhost:5000/ringba-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "campaignName": "Your Campaign Name",
    "targetName": "Your Target Name",
    "callerId": "TEST_123",
    "timestamp": "2024-01-01T12:00:00Z"
  }'
```

### 4. Deployment Options

#### Option A: Railway (Recommended)
1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy**:
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Set Environment Variables**:
   ```bash
   railway variables set RINGBA_CAMPAIGN_NAME="Your Campaign Name"
   railway variables set RINGBA_TARGET_NAME="Your Target Name"
   railway variables set GOOGLE_SHEET_ID="your_sheet_id"
   railway variables set SLACK_WEBHOOK_URL="your_webhook_url"
   ```

#### Option B: Render
1. **Connect your GitHub repository**
2. **Create a new Web Service**
3. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn main:app`
   - Add environment variables in the dashboard

#### Option C: Heroku
1. **Install Heroku CLI**
2. **Deploy**:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

3. **Set Config Vars**:
   ```bash
   heroku config:set RINGBA_CAMPAIGN_NAME="Your Campaign Name"
   heroku config:set GOOGLE_SHEET_ID="your_sheet_id"
   heroku config:set SLACK_WEBHOOK_URL="your_webhook_url"
   ```

### 5. Ringba Webhook Configuration

1. **In Ringba Dashboard**:
   - Go to your campaign settings
   - Find webhook configuration
   - Add your deployed URL: `https://your-app.railway.app/ringba-webhook`

2. **Test the Integration**:
   - Make a test call through Ringba
   - Check your Google Sheet for new entries
   - Verify Slack notifications

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `RINGBA_CAMPAIGN_NAME` | Campaign name to filter | Yes |
| `RINGBA_TARGET_NAME` | Target name to filter | Yes |
| `GOOGLE_SHEET_ID` | Google Sheet ID | Yes |
| `GOOGLE_SHEET_TAB` | Sheet tab name (default: Sheet1) | No |
| `GOOGLE_CREDS_FILE` | Path to credentials.json | No |
| `SLACK_WEBHOOK_URL` | Slack incoming webhook URL | Yes |
| `FLASK_ENV` | Flask environment (development/production) | No |
| `FLASK_DEBUG` | Enable debug mode (True/False) | No |
| `PORT` | Port to run on (default: 5000) | No |

## Google Sheet Structure

The application automatically creates headers and appends rows with this structure:

| Column | Description | Auto-filled |
|--------|-------------|-------------|
| Time of call | UTC timestamp | ✅ |
| CallerID | From Ringba data | ✅ |
| Agent Name | For manual entry | ❌ |
| Status | For manual updates | ❌ |
| Notes | For manual notes | ❌ |

## Monitoring and Maintenance

### Health Check
```bash
curl https://your-app.railway.app/
```

### Logs
- **Railway**: `railway logs`
- **Render**: Dashboard > Logs
- **Heroku**: `heroku logs --tail`

### Keeping the App Running 24/7

1. **Use a reliable platform** (Railway, Render, Heroku)
2. **Set up monitoring**:
   - Health check endpoints
   - Error notifications
   - Uptime monitoring

3. **Regular maintenance**:
   - Monitor logs for errors
   - Check Google Sheet permissions
   - Verify Slack webhook is active

## Troubleshooting

### Common Issues

1. **Google Sheets Permission Error**:
   - Ensure service account has edit access
   - Check credentials.json is valid

2. **Slack Notifications Not Working**:
   - Verify webhook URL is correct
   - Check if webhook is still active

3. **Webhook Not Receiving Data**:
   - Verify URL is accessible
   - Check Ringba webhook configuration
   - Test with curl or Postman

4. **Filter Not Working**:
   - Check campaign and target names match exactly
   - Verify case sensitivity

### Debug Mode
Set `FLASK_DEBUG=True` in your environment variables for detailed error messages.

## Support

For issues or questions:
1. Check the logs for error messages
2. Verify all environment variables are set correctly
3. Test individual components (Google Sheets, Slack) separately
4. Use the test script to verify webhook functionality

## License

This project is open source and available under the MIT License.



