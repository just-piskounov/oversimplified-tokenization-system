# 🛡️ PCI-DSS Tokenization System - Educational Project

Welcome to this educational project that demonstrates how **credit card tokenization** works in the real world! This is a simplified but functional implementation of a PCI-DSS compliant tokenization system that helps you understand how companies like Stripe, PayPal, and Square handle sensitive payment data.

> 🎓 **Perfect for learning:** Computer Science students, junior developers, or anyone curious about payment security!

---

## 🤔 What Problem Does This Solve?

### The Credit Card Storage Problem

Imagine you're building an e-commerce website. When customers enter their credit card numbers, you face a huge dilemma:

- ❌ **Store the card numbers directly?** → HUGE security risk + legal compliance nightmare
- ❌ **Don't store them at all?** → Customers have to re-enter cards every time
- ✅ **Use tokenization!** → Store safe "tokens" instead of real card numbers

### Real-World Example

```
Customer enters: 4532 1234 5678 9012
Your system stores: tok_a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

The real card number is safely locked away in an encrypted vault, and you only work with the harmless token!

---

## 🏗️ How This System Works

### The Big Picture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│  Merchant App   │◄──►│ Token Server    │◄──►│ Encrypted Vault │
│  (Your Store)   │    │   (FastAPI)     │    │   (JSON File)   │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Step-by-Step Flow

1. **Customer enters card:** `4532123456789012`
2. **Merchant app sends to token server:** "Please tokenize this card"
3. **Token server:**
   - Generates random token: `tok_abc123...`
   - Encrypts card with AES-256: `encrypted_blob`
   - Stores mapping: `tok_abc123 → encrypted_blob`
4. **Returns token to merchant:** `tok_abc123...`
5. **Merchant stores token** (safe!) and forgets the real card number

Later, when processing a payment:
1. **Merchant sends:** "Charge $50 to token `tok_abc123`"
2. **Token server:** Looks up token → decrypts → processes payment
3. **Merchant never sees the real card number again!**

---

## 📁 Project Structure Explained

```
pci-tokenization-project/
├── 🌐 token_server/              # The secure tokenization service
│   ├── main.py                   # FastAPI endpoints (/tokenize, /charge, etc.)
│   ├── vault.py                  # Encryption/decryption + storage
│   ├── auth.py                   # API authentication
│   ├── token_logic.py            # Token generation (UUID-based)
│   └── logger.py                 # Audit logging for compliance
├── 💻 merchant_cli/              # Simulates your e-commerce app
│   ├── cli.py                    # Interactive command-line interface
│   └── api_client.py             # HTTP client to talk to token server
├── 💾 data/                      # Where everything gets stored
│   ├── token_map.json            # Token → Encrypted Card mappings
│   ├── audit.log                 # Security audit trail
│   └── purchases.json            # Transaction history
├── 🔧 Configuration files
│   ├── .env                      # Secret keys and tokens
│   ├── requirements.txt          # Python dependencies
│   └── run.sh                    # One-command startup script
└── 📚 README.md                  # This file!
```

---

## 🔐 Security Features Explained

### 1. **AES-256 Encryption** 🔒
- **What it is:** Military-grade encryption standard
- **Why it matters:** Even if someone steals your `token_map.json`, they can't read the card numbers
- **How it works:** Uses a 256-bit key to scramble card numbers into unreadable gibberish

### 2. **Token-Based Architecture** 🎫
- **What it is:** Replace sensitive data with meaningless tokens
- **Why it matters:** Tokens are worthless to hackers - they can't be used for purchases
- **How it works:** Random UUIDs like `tok_12345-abcd-...` that map to encrypted cards

### 3. **API Authentication** 🔑
- **What it is:** Bearer token authentication for API access
- **Why it matters:** Only authorized merchants can tokenize/detokenize
- **How it works:** Every API request must include `Authorization: Bearer supersecuremerchant123`

### 4. **Audit Logging** 📋
- **What it is:** Every operation gets logged with timestamps
- **Why it matters:** PCI-DSS compliance requires detailed audit trails
- **How it works:** All tokenizations, charges, and auth failures get recorded

### 5. **Data Separation** 🏢
- **What it is:** Merchant app never directly accesses the card vault
- **Why it matters:** Limits blast radius if merchant system gets compromised
- **How it works:** All sensitive operations go through the secure token server

---

## 🚀 Getting Started - Step by Step

### Prerequisites
- Python 3.8+ installed
- Basic command line knowledge
- 10 minutes of your time!

### Step 1: Download and Setup

```bash
# Clone or download this project
git clone <your-repo-url>
cd pci-tokenization-project

# Create isolated Python environment
python -m venv venv

# Activate it (Linux/Mac)
source venv/bin/activate

# Or on Windows
venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **FastAPI:** Modern Python web framework
- **Uvicorn:** ASGI server to run FastAPI
- **PyCryptodome:** Encryption library
- **Requests:** HTTP client for API calls
- **Other supporting libraries**

### Step 3: Configuration

The `.env` file contains your secret keys:

```env
AES_KEY=fdc90123ed2f9b2f99d1e1e6af1ad312  # 32-byte encryption key
AUTH_TOKEN=supersecuremerchant123          # API authentication token
```

> 🔐 **In production:** These would be stored in secure key management systems, not plain text files!

### Step 4: Launch Everything!

```bash
./run.sh
```

This script:
1. ✅ Activates your Python environment
2. ✅ Creates necessary data directories
3. ✅ Starts the FastAPI tokenization server
4. ✅ Launches the interactive merchant CLI
5. ✅ Handles cleanup when you're done

---

## 💳 Using the System - Interactive Demo

When you run `./run.sh`, you'll see this menu:

```
🔐 PCI Tokenization CLI
1. Tokenize PAN
2. Detokenize Token  
3. Charge Token
0. Exit
>
```

### Demo Scenario: Online Store Checkout

Let's simulate a customer buying something from your online store:

#### Step 1: Customer Enters Card (Tokenization)
```
> 1
Enter card number (PAN): 4532123456789012
✅ Token generated: tok_a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**What just happened:**
- Card number sent to token server via HTTPS
- Server encrypted card with AES-256
- Generated random token as substitute
- Stored mapping in encrypted vault
- Returned safe token to your app

#### Step 2: Customer Completes Purchase (Charging)
```
> 3  
Enter token: tok_a1b2c3d4-e5f6-7890-abcd-ef1234567890
Enter amount (e.g. 49.99): 99.99
💰 Successfully charged $99.99 to token tok_a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**What just happened:**
- Your app sent charge request with token (not card!)
- Token server looked up token → found encrypted card
- Decrypted card number for payment processing
- Recorded transaction in purchase log
- Your app never saw the real card number!

#### Step 3: Customer Service Lookup (Detokenization)
```
> 2
Enter token: tok_a1b2c3d4-e5f6-7890-abcd-ef1234567890  
✅ PAN retrieved: 4532123456789012
```

**What just happened:**
- Customer service rep needs to verify card for refund
- System safely retrieves card using token
- Only authorized systems can detokenize
- Action gets logged for compliance

---

## 📊 Understanding the Data Files

After running the demo, check out these generated files:

### `data/token_map.json` - The Encrypted Vault
```json
{
  "tok_39bdeb06-c889-4933-a3f2-7d889a6ea8c8": "yWn7XQm6f5rt0g+rdMoX7UUlVdJNBlXVgwl5g4bi0lk=",
  "tok_d46325ff-1d8f-47fe-b5c4-dd51b90fff50": "ye7di4oSUrLK9GTEDRe2/E/71AMujEZQdGrfDhemh50="
}
```

**What you're seeing:** 
- Keys = meaningless tokens
- Values = base64-encoded encrypted card numbers
- Even if stolen, this data is useless without the AES key!

### `data/audit.log` - Compliance Trail
```
2025-07-19T09:52:49.928633 - TOKENIZED - tok_39bdeb06-c889-4933-a3f2-7d889a6ea8c8
2025-07-19T09:58:34.322474 - CHARGED - tok_d46325ff-1d8f-47fe-b5c4-dd51b90fff50 - Amount: 99.99
```

**What you're seeing:**
- Timestamps for every sensitive operation
- Action types (TOKENIZED, CHARGED, DETOKENIZED, etc.)
- Token IDs and relevant details
- Critical for PCI-DSS compliance audits

### `data/purchases.json` - Transaction History
```json
[
  {
    "token": "tok_d46325ff-1d8f-47fe-b5c4-dd51b90fff50",
    "amount": "99.99"
  }
]
```

**What you're seeing:**
- Business transaction records
- Notice: No card numbers stored here!
- Safe to back up, analyze, share with accounting

---

## 🔍 Code Deep Dive - How It All Works

### The FastAPI Token Server (`token_server/main.py`)

```python
@app.post("/tokenize")
async def tokenize(request: Request, body: TokenizeRequest):
    # 1. Check if request is authorized
    auth_header = request.headers.get("Authorization")
    if not is_authorized(auth_header):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # 2. Generate random token
    token = generate_token()  # Creates "tok_" + UUID
    
    # 3. Encrypt the card number
    encrypted = encrypt_pan(body.pan)  # AES-256 encryption
    
    # 4. Store the mapping safely
    store_mapping(token, encrypted)
    
    # 5. Log for compliance
    log("TOKENIZED", token)
    
    # 6. Return token (never the card!)
    return {"token": token}
```

### The Encryption Vault (`token_server/vault.py`)

```python
def encrypt_pan(pan: str) -> str:
    # Create AES cipher in EAX mode (authenticated encryption)
    cipher = AES.new(KEY, AES.MODE_EAX)
    
    # Get random nonce (number used once)
    nonce = cipher.nonce
    
    # Encrypt and authenticate the card number
    ciphertext, tag = cipher.encrypt_and_digest(pan.encode())
    
    # Return base64-encoded (nonce + ciphertext)
    return b64encode(nonce + ciphertext).decode()
```

**Why EAX mode?**
- Provides both encryption AND authentication
- Prevents tampering with encrypted data
- Industry best practice for sensitive data

### The Merchant Client (`merchant_cli/api_client.py`)

```python
def request_token(pan: str):
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",  # Authenticate
        "Content-Type": "application/json"
    }
    body = {"pan": pan}
    
    # Send HTTPS request to token server
    response = requests.post(f"{API_URL}/tokenize", 
                           json=body, headers=headers)
    
    return response.json()["token"]
```

---

## 🎯 Learning Objectives - What You'll Understand

After exploring this project, you'll have hands-on experience with:

### 🔐 **Cryptography Concepts**
- **Symmetric encryption** (AES-256)
- **Authenticated encryption** (EAX mode)
- **Key management** basics
- **Base64 encoding** for data transport

### 🌐 **API Security**
- **Bearer token authentication**
- **HTTPS-first design**
- **Input validation**
- **Error handling** without information leakage

### 🏗️ **System Architecture**
- **Microservices** separation
- **Data isolation** principles
- **Client-server** communication
- **Stateless** API design

### 📋 **Compliance & Logging**
- **Audit trail** requirements
- **PCI-DSS** basic principles
- **Operational logging**
- **Security monitoring**

### 💻 **Practical Skills**
- **FastAPI** web framework
- **Python** async programming
- **JSON** data handling
- **Environment** configuration
- **Shell scripting**

---

## 🌟 Real-World Applications

### Where Is This Used?

1. **Payment Processors**
   - Stripe, Square, PayPal
   - Store millions of tokenized cards
   - Process billions in transactions

2. **E-commerce Platforms**
   - Amazon, Shopify, WooCommerce
   - Enable "save card" features safely
   - Reduce PCI compliance scope

3. **Mobile Payment Apps**
   - Apple Pay, Google Pay, Samsung Pay
   - Tokenize cards for NFC payments
   - Add extra security layers

4. **Subscription Services**
   - Netflix, Spotify, Adobe
   - Store payment methods securely
   - Process recurring charges

### Career Applications

Understanding tokenization helps with:
- **Backend developer** roles
- **DevOps/Security** positions
- **Fintech** company interviews
- **Payment processing** projects
- **Compliance** consulting

---

## 🔧 Extending This Project

### Easy Additions (Beginner)

1. **Token Expiration**
   ```python
   # Add expiry timestamp to tokens
   {"token": "tok_123", "expires": "2025-12-31T23:59:59Z"}
   ```

2. **Multiple Merchants**
   ```python
   # Different API keys for different stores
   MERCHANT_TOKENS = {
       "store_a": "token_123",
       "store_b": "token_456"
   }
   ```

3. **Input Validation**
   ```python
   def validate_pan(pan: str) -> bool:
       # Luhn algorithm check
       # Length validation
       # Format validation
   ```

### Intermediate Additions

4. **Database Storage**
   - Replace JSON files with PostgreSQL/MySQL
   - Add proper indexing and transactions
   - Implement connection pooling

5. **HTTPS/TLS**
   - Add SSL certificates
   - Force HTTPS-only communication
   - Implement certificate pinning

6. **Rate Limiting**
   - Prevent API abuse
   - Per-merchant quotas
   - DDoS protection

### Advanced Additions (Expert)

7. **Hardware Security Modules (HSM)**
   - Store encryption keys in dedicated hardware
   - FIPS 140-2 Level 3 compliance
   - Cloud HSM integration

8. **Key Rotation**
   - Automatic key rotation schedules
   - Zero-downtime key updates
   - Key versioning and migration

9. **Multi-Region Deployment**
   - Geographic data replication
   - Disaster recovery
   - Performance optimization

---

## 🚨 Security Disclaimers

### ⚠️ This Is Educational Code

**DO NOT use this code in production without significant hardening:**

- **Missing features:** TLS/HTTPS, proper key management, input sanitization, rate limiting, monitoring, etc.
- **Simplified storage:** Real systems use hardened databases, not JSON files
- **Basic authentication:** Production needs OAuth2, JWT, multi-factor auth, etc.
- **No compliance auditing:** Real PCI-DSS compliance requires extensive third-party validation

### ✅ What This Teaches You

- Core tokenization concepts
- API security fundamentals  
- Encryption best practices
- System architecture patterns
- Compliance logging basics

### 🏢 Production-Ready Alternatives

If you need real tokenization:
- **Stripe Elements** - Frontend + backend tokenization
- **AWS Payment Cryptography** - Enterprise-grade tokenization
- **Adyen** - Global payment platform
- **Braintree** - PayPal's tokenization service

---

## 📚 Additional Learning Resources

### Books
- **"Payment Card Industry Data Security Standard"** (Official PCI-DSS Guide)

### Online Courses
- **Coursera:** "Cryptography" by Stanford University
- **edX:** "Introduction to Cybersecurity" by NYU
- **Pluralsight:** "Payment Card Industry (PCI) Compliance" 

### Documentation
- **PCI Security Standards Council:** Official PCI-DSS documentation
- **NIST Cybersecurity Framework:** Government security guidelines
- **OWASP:** Web application security best practices

### Practice Platforms
- **HackTheBox:** Cybersecurity challenges
- **TryHackMe:** Beginner-friendly security labs
- **PentesterLab:** Web application security testing

---

## 🤝 Contributing & Questions

### Found a Bug? 🐛
- Open an issue with detailed steps to reproduce
- Include your OS, Python version, and error messages
- Check existing issues first to avoid duplicates

### Want to Add Features? ✨
- Fork the repository
- Create a feature branch
- Add tests for new functionality
- Submit a pull request with clear description

### Have Questions? ❓
- Check this README first (seriously, it's comprehensive!)
- Search existing issues and discussions
- Create a new issue with "Question:" prefix
- Be specific about what you're trying to understand

### Educational Use 🎓
This project is specifically designed for learning. Feel free to:
- Adapt for different programming languages
- Use concepts for production

---

## 📜 License & Legal

### MIT License
This project is released under the MIT License - use it freely for educational purposes, but remember the security disclaimers above!

### Legal Notice
- **Not production-ready:** This code is for educational purposes only
- **No warranty:** Use at your own risk
- **Compliance:** Consult security professionals for real PCI-DSS compliance
- **Liability:** Authors not responsible for any misuse or security breaches

---

## 🎉 Final Words

Congratulations! You've just explored a complete tokenization system that mirrors what billion-dollar companies use to protect payment data. You've learned about:

- **Modern cryptography** in practice
- **Secure API design** patterns  
- **Payment industry** standards
- **System architecture** principles
- **Compliance** requirements

---

