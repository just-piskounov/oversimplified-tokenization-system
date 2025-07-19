import requests

API_URL = "http://localhost:8000"
AUTH_TOKEN = "supersecuremerchant123"

def request_token(pan: str):
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    body = {"pan": pan}
    try:
        response = requests.post(f"{API_URL}/tokenize", json=body, headers=headers)
        response.raise_for_status()
        return response.json()["token"]
    except requests.HTTPError as e:
        print("Tokenization failed:", e.response.text)
        return None

def request_detokenization(token: str):
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    body = {"token": token}
    try:
        response = requests.post(f"{API_URL}/detokenize", json=body, headers=headers)
        response.raise_for_status()
        return response.json()["pan"]
    except requests.HTTPError as e:
        print("De-tokenization failed:", e.response.text)
        return None

def request_charge(token: str, amount: str):
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    body = {"token": token, "amount": amount}
    try:
        response = requests.post(f"{API_URL}/charge", json=body, headers=headers)
        response.raise_for_status()
        return response.json()["message"]
    except requests.HTTPError as e:
        print("Charge failed:", e.response.text)
        return None

