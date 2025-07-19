import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_URL = "http://localhost:8000"
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "supersecuremerchant123")

def request_token(pan: str):
    """Request tokenization of a PAN"""
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    body = {"pan": pan}
    
    try:
        print(f"🔄 Sending tokenization request...")
        response = requests.post(f"{API_URL}/tokenize", json=body, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.json()["token"]
        else:
            print(f"❌ Tokenization failed (HTTP {response.status_code})")
            try:
                error_detail = response.json().get("detail", "Unknown error")
                print(f"   Error: {error_detail}")
            except:
                print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ Request timeout - server may be slow or down")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - is the server running?")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def request_detokenization(token: str):
    """Request detokenization of a token"""
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    body = {"token": token}
    
    try:
        print(f"🔄 Sending detokenization request...")
        response = requests.post(f"{API_URL}/detokenize", json=body, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.json()["pan"]
        else:
            print(f"❌ Detokenization failed (HTTP {response.status_code})")
            try:
                error_detail = response.json().get("detail", "Unknown error")
                print(f"   Error: {error_detail}")
            except:
                print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ Request timeout - server may be slow or down")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - is the server running?")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def request_charge(token: str, amount: str):
    """Request a charge against a token"""
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    body = {"token": token, "amount": amount}
    
    try:
        print(f"🔄 Sending charge request...")
        response = requests.post(f"{API_URL}/charge", json=body, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.json()["message"]
        else:
            print(f"❌ Charge failed (HTTP {response.status_code})")
            try:
                error_detail = response.json().get("detail", "Unknown error")
                print(f"   Error: {error_detail}")
            except:
                print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ Request timeout - server may be slow or down")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - is the server running?")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def test_server():
    """Test server connectivity"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False
