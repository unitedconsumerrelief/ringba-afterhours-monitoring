#!/usr/bin/env python3
"""
Test script to simulate Ringba webhook calls for After Hours Monitor
Usage: python test_webhook.py
"""

import requests
import json
from datetime import datetime

# Configuration
WEBHOOK_URL = "http://localhost:5000/ringba-webhook"  # Change this to your deployed URL

def test_valid_webhook():
    """Test a webhook that should pass the filter (valid target, within hours)"""
    payload = {
        "targetName": "TA7a8e20272b90487c8d420370c8477992",
        "callerId": "TEST_CALLER_123",
        "timestamp": datetime.utcnow().isoformat(),
        "duration": 120,
        "status": "completed"
    }
    
    print("Testing valid webhook (valid target)...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(WEBHOOK_URL, json=payload)
    print(f"Response Status: {response.status_code}")
    print(f"Response Body: {response.text}")
    print("-" * 50)

def test_no_value_webhook():
    """Test a webhook that should be filtered out (No value target)"""
    payload = {
        "targetName": "No value",
        "callerId": "NO_VALUE_CALLER_456",
        "timestamp": datetime.utcnow().isoformat(),
        "duration": 60,
        "status": "completed"
    }
    
    print("Testing No value webhook (should be filtered)...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(WEBHOOK_URL, json=payload)
    print(f"Response Status: {response.status_code}")
    print(f"Response Body: {response.text}")
    print("-" * 50)

def test_empty_target_webhook():
    """Test a webhook that should be filtered out (empty target)"""
    payload = {
        "targetName": "",
        "callerId": "EMPTY_TARGET_CALLER_789",
        "timestamp": datetime.utcnow().isoformat(),
        "duration": 30,
        "status": "completed"
    }
    
    print("Testing empty target webhook (should be filtered)...")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(WEBHOOK_URL, json=payload)
    print(f"Response Status: {response.status_code}")
    print(f"Response Body: {response.text}")
    print("-" * 50)

def test_health_check():
    """Test the health check endpoint"""
    health_url = WEBHOOK_URL.replace("/ringba-webhook", "/")
    
    print("Testing health check...")
    response = requests.get(health_url)
    print(f"Response Status: {response.status_code}")
    print(f"Response Body: {response.text}")
    print("-" * 50)

if __name__ == "__main__":
    print("🌙 Ringba After Hours Monitor Test Script")
    print("=" * 50)
    print("Note: This will only send notifications if run during monitoring hours (6pm EST - 9am EST)")
    print("=" * 50)
    
    # Test health check first
    test_health_check()
    
    # Test empty target webhook (should be filtered)
    test_empty_target_webhook()
    
    # Test No value webhook (should be filtered)
    test_no_value_webhook()
    
    # Test valid webhook (should be processed if within hours)
    test_valid_webhook()
    
    print("✅ Testing complete!")
    print("\nCheck your Slack channel for results (only if within monitoring hours).")
