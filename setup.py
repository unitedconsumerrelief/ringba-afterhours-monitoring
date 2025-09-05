#!/usr/bin/env python3
"""
Setup script for Ringba Webhook Handler
This script helps you configure the application for first-time use.
"""

import os
import json
from pathlib import Path

def create_env_file():
    """Create .env file from template"""
    if not os.path.exists('.env'):
        print("📝 Creating .env file...")
        with open('env.example', 'r') as example:
            content = example.read()
        
        with open('.env', 'w') as env_file:
            env_file.write(content)
        
        print("✅ .env file created! Please edit it with your actual values.")
    else:
        print("ℹ️  .env file already exists.")

def check_credentials():
    """Check if Google credentials file exists"""
    if not os.path.exists('credentials.json'):
        print("⚠️  Google credentials.json not found!")
        print("📋 Please follow these steps:")
        print("   1. Go to Google Cloud Console")
        print("   2. Create a service account")
        print("   3. Download the JSON key file")
        print("   4. Save it as 'credentials.json' in this directory")
        return False
    else:
        print("✅ Google credentials.json found!")
        return True

def validate_env_vars():
    """Check if required environment variables are set"""
    required_vars = [
        'RINGBA_CAMPAIGN_NAME',
        'RINGBA_TARGET_NAME', 
        'GOOGLE_SHEET_ID',
        'SLACK_WEBHOOK_URL'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("⚠️  Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n📋 Please set these in your .env file")
        return False
    else:
        print("✅ All required environment variables are set!")
        return True

def test_google_sheets():
    """Test Google Sheets connection"""
    try:
        from google_sheets import append_row_to_sheet
        result = append_row_to_sheet("TEST_TIME", "TEST_CALLER")
        if result:
            print("✅ Google Sheets connection successful!")
            return True
        else:
            print("❌ Google Sheets connection failed!")
            return False
    except Exception as e:
        print(f"❌ Google Sheets test failed: {str(e)}")
        return False

def test_slack():
    """Test Slack webhook"""
    try:
        from slack_notify import send_slack_alert
        result = send_slack_alert("TEST_CALLER", "TEST_TIME", "https://example.com")
        if result:
            print("✅ Slack webhook test successful!")
            return True
        else:
            print("❌ Slack webhook test failed!")
            return False
    except Exception as e:
        print(f"❌ Slack test failed: {str(e)}")
        return False

def main():
    print("🚀 Ringba Webhook Handler Setup")
    print("=" * 40)
    
    # Create .env file
    create_env_file()
    
    # Check credentials
    creds_ok = check_credentials()
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Validate environment variables
    env_ok = validate_env_vars()
    
    print("\n🧪 Running Tests...")
    
    # Test Google Sheets
    sheets_ok = False
    if creds_ok and env_ok:
        sheets_ok = test_google_sheets()
    
    # Test Slack
    slack_ok = False
    if env_ok:
        slack_ok = test_slack()
    
    print("\n📊 Setup Summary:")
    print(f"   Google Credentials: {'✅' if creds_ok else '❌'}")
    print(f"   Environment Variables: {'✅' if env_ok else '❌'}")
    print(f"   Google Sheets: {'✅' if sheets_ok else '❌'}")
    print(f"   Slack Webhook: {'✅' if slack_ok else '❌'}")
    
    if all([creds_ok, env_ok, sheets_ok, slack_ok]):
        print("\n🎉 Setup complete! Your app is ready to run.")
        print("💡 Next steps:")
        print("   1. Run: python main.py")
        print("   2. Test with: python test_webhook.py")
        print("   3. Deploy to Railway/Render/Heroku")
    else:
        print("\n⚠️  Setup incomplete. Please fix the issues above.")
        print("💡 Check the README.md for detailed setup instructions.")

if __name__ == "__main__":
    main()



