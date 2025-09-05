import socket
import requests
import time

def test_port(port):
    print(f"Testing port {port}...")
    
    # Test if port is open
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('192.168.254.100', port))
    sock.close()
    
    if result == 0:
        print(f"✅ Port {port} is open")
        return True
    else:
        print(f"❌ Port {port} is closed")
        return False

def test_webhook(port):
    url = f"http://192.168.254.100:{port}/ringba-webhook"
    payload = {
        "campaignName": "SPANISH DEBT | 3.5 STANDARD | 01292025",
        "targetName": "-no value-",
        "callerId": "TEST_PORT_123"
    }
    
    try:
        start_time = time.time()
        response = requests.post(url, json=payload, timeout=15)
        end_time = time.time()
        
        print(f"✅ Webhook test successful in {end_time - start_time:.2f} seconds")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Webhook test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing different ports for Ringba webhook...")
    print("=" * 50)
    
    # Test common ports
    ports = [5000, 80, 8080, 3000]
    
    for port in ports:
        if test_port(port):
            test_webhook(port)
        print("-" * 30)

