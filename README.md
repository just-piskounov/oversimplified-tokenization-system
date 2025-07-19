# 🛡️ PCI-DSS Tokenization System (Python)

This project demonstrates a simplified **PCI-DSS compliant tokenization system**, built using:

- 🔧 **FastAPI** (secure backend microservice)
- 💻 **Python CLI** (simulated merchant app)
- 🔐 **AES-256 encryption** (PAN vault)
- 🧾 **Audit logging** (per PCI guidelines)

> ⚠️ This project is for educational use only. Not production-hardened.

---

## 🗂️ Project Structure

```
pci-tokenization-project/
├── token_server/         # FastAPI secure tokenization service
├── merchant_cli/         # CLI client used by merchant
├── data/                 # Encrypted vault, logs, token map
├── .env                  # AES key and API token
├── requirements.txt
├── run.sh                # Starts the whole system
└── README.md
```

---

## 🔐 PCI-DSS Compliance Features

- PANs encrypted with **AES-256** in EAX mode
- **Tokenized PANs** are random UUIDs
- Only authenticated clients can access `/tokenize`, `/detokenize`, and `/charge`
- **No CVV** or expiry date stored (per PCI rule 3.2)
- **Audit log** and purchase ledger recorded
- Merchant never accesses PANs or vault directly

---

## 🚀 Getting Started

### 1. Clone the project

```bash
git clone <your_repo_url>
cd pci-tokenization-project
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

Create a `.env` file:

```env
AES_KEY=fdc90123ed2f9b2f99d1e1e6af1ad312
AUTH_TOKEN=supersecuremerchant123
```

> AES_KEY must be 64 hex characters (32 bytes)

---

## ▶️ Run Everything

Just run the script:

```bash
./run.sh
```

You’ll see:

- ✅ Tokenization server starting
- ✅ CLI merchant prompt
- ✅ API and vault interaction

---

## 💳 CLI Options

```
1. Tokenize PAN
2. Detokenize Token
3. Charge Token
```

All interactions are logged in:

- `data/audit.log`
- `data/token_map.json`
- `data/purchases.json`

---

## 📚 Learnings

You’ll understand:
- How to build an API from scratch
- How to handle secure tokenization and storage
- How to isolate merchant from sensitive data
- How to simulate PCI-compliant flows in Python

---

## 🧪 Want More?

Want to add:
- Token expiration?
- TLS (HTTPS)?
- Multiple merchant keys?

Open an issue or extend the system 🚀

---

## 🧾 License

MIT License — use freely, but not for production card data.

