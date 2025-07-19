import os
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
from dotenv import load_dotenv

load_dotenv()
KEY = bytes.fromhex(os.getenv("AES_KEY"))

VAULT_FILE = "data/token_map.json"

def encrypt_pan(pan: str) -> str:
    cipher = AES.new(KEY, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(pan.encode())
    return b64encode(nonce + ciphertext).decode()

def decrypt_pan(blob: str) -> str:
    """Fixed decryption function with proper nonce handling"""
    raw = b64decode(blob)
    nonce = raw[:16]  # Extract nonce (first 16 bytes)
    ciphertext = raw[16:]  # Extract ciphertext (remaining bytes)
    cipher = AES.new(KEY, AES.MODE_EAX, nonce)
    return cipher.decrypt(ciphertext).decode()

def store_mapping(token: str, encrypted_pan: str):
    os.makedirs("data", exist_ok=True)
    if os.path.exists(VAULT_FILE):
        with open(VAULT_FILE, "r") as f:
            db = json.load(f)
    else:
        db = {}
 
    db[token] = encrypted_pan
    with open(VAULT_FILE, "w") as f:
        json.dump(db, f, indent=2)

def get_encrypted_pan(token: str) -> str:
    if not os.path.exists(VAULT_FILE):
        return None
    with open(VAULT_FILE, "r") as f:
        db = json.load(f)
    return db.get(token)

def record_purchase(token: str, amount: str):
    """Fixed purchase recording with proper file handling"""
    purchase_log = "data/purchases.json"
    os.makedirs("data", exist_ok=True)
    
    # Handle empty or non-existent file
    if os.path.exists(purchase_log) and os.path.getsize(purchase_log) > 0:
        try:
            with open(purchase_log, "r") as f:
                purchases = json.load(f)
        except json.JSONDecodeError:
            # File exists but is empty/corrupted, start fresh
            purchases = []
    else:
        purchases = []

    purchases.append({"token": token, "amount": amount})
    with open(purchase_log, "w") as f:
        json.dump(purchases, f, indent=2)
