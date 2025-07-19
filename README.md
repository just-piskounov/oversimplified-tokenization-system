# 🔐 PCI Tokenization System

A simple educational project showing how credit card tokenization works.

## What is Tokenization?

Instead of storing credit card numbers directly (risky), we replace them with safe tokens:

```
Card: 4532123456789012  →  Token: tok_abc123-def456
```

The real card is encrypted and stored securely. Your app only sees the harmless token.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start everything
./run.sh
```

That's it! The system will start and give you an interactive menu.

## How It Works

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Your App  │───►│ Token Server│───►│ Vault (AES) │
│             │    │  (FastAPI)  │    │  Encrypted  │
└─────────────┘    └─────────────┘    └─────────────┘
```

1. **Tokenize**: Send card → Get safe token back
2. **Charge**: Send token + amount → Process payment  
3. **Your app never stores real card numbers**

## Example Usage

```
🔐 PCI Tokenization CLI
1. Tokenize PAN
2. Detokenize Token  
3. Charge Token
0. Exit

> 1
Enter card: 4532123456789012
✅ Token: tok_a1b2c3d4-e5f6-7890-abcd-ef1234567890

> 3
Enter token: tok_a1b2c3d4-e5f6-7890-abcd-ef1234567890
Enter amount: 99.99
💰 Successfully charged $99.99
```

## Project Structure

```
├── token_server/     # Secure tokenization API
├── merchant_cli/     # Your app (simulated)
├── data/            # Encrypted storage
└── .env            # Secret keys
```

## Security Features

- **AES-256 Encryption**: Military-grade card protection
- **Token Isolation**: Apps never see real cards
- **API Authentication**: Bearer token security
- **Audit Logging**: Every action tracked

## Real-World Usage

This is how companies like Stripe, PayPal, and Square protect billions of cards:

- **E-commerce**: Save cards without PCI compliance nightmare
- **Subscriptions**: Recurring billing with tokens
- **Mobile Apps**: Secure NFC payments

## ⚠️ Educational Only

This is for learning. Production systems need:
- HTTPS/TLS encryption
- Hardware security modules
- Professional security audits
- Real PCI-DSS compliance

## Learn More

- **Payment Security**: Understanding tokenization concepts
- **API Design**: FastAPI + authentication patterns  
- **Cryptography**: AES encryption in practice
- **Compliance**: PCI-DSS basics

---

*Built for learning how payment tokenization works under the hood* 🎓
