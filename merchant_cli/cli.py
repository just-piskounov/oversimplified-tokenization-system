from api_client import (
    request_token, request_detokenization, request_charge
)

def main():
    print("🔐 PCI Tokenization CLI")
    print("1. Tokenize PAN")
    print("2. Detokenize Token")
    print("3. Charge Token")
    choice = input("> ").strip()

    if choice == "1":
        pan = input("Enter card number (PAN): ").strip()
        if not pan.isdigit():
            print("Invalid PAN. Must be numbers only.")
            return
        token = request_token(pan)
        if token:
            print("✅ Token generated:", token)
        else:
            print("❌ Tokenization failed.")

    elif choice == "2":
        token = input("Enter token: ").strip()
        pan = request_detokenization(token)
        if pan:
            print("✅ PAN retrieved:", pan)
        else:
            print("❌ Detokenization failed.")

    elif choice == "3":
        token = input("Enter token: ").strip()
        amount = input("Enter amount (e.g. 49.99): ").strip()
        response = request_charge(token, amount)
        if response:
            print("💰", response)
        else:
            print("❌ Charge failed.")

