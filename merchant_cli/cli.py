import sys
import os

# Add the parent directory to the Python path so we can import api_client
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_client import (
    request_token, request_detokenization, request_charge
)

def main():
    print("🔐 PCI-DSS Tokenization System")
    print("=" * 40)
    
    while True:
        print("\n💳 Available Operations:")
        print("1. 🔒 Tokenize PAN (Convert card number to token)")
        print("2. 🔓 Detokenize Token (Get card number from token)")
        print("3. 💰 Charge Token (Process payment)")
        print("0. 🚪 Exit")
        print("-" * 40)
        
        choice = input("Select option (0-3): ").strip()

        if choice == "1":
            print("\n🔒 TOKENIZE PAN")
            pan = input("Enter card number (digits only): ").strip()
            
            # Basic validation
            if not pan:
                print("❌ Error: PAN cannot be empty")
                continue
            if not pan.isdigit():
                print("❌ Error: PAN must contain only digits")
                continue
            if len(pan) < 13 or len(pan) > 19:
                print("❌ Error: PAN must be 13-19 digits long")
                continue
                
            print(f"🔄 Tokenizing PAN: {pan[:4]}****{pan[-4:]}")
            token = request_token(pan)
            if token:
                print(f"✅ Token generated successfully!")
                print(f"🎫 Token: {token}")
                print(f"💡 Save this token to process charges later")
            else:
                print("❌ Tokenization failed - check server logs")

        elif choice == "2":
            print("\n🔓 DETOKENIZE TOKEN")
            token = input("Enter token: ").strip()
            
            if not token:
                print("❌ Error: Token cannot be empty")
                continue
                
            print("🔄 Detokenizing token...")
            pan = request_detokenization(token)
            if pan:
                print(f"✅ PAN retrieved successfully!")
                print(f"💳 Card number: {pan[:4]}****{pan[-4:]}")
                print(f"⚠️  Full PAN: {pan} (shown for demo purposes)")
            else:
                print("❌ Detokenization failed - token may not exist")

        elif choice == "3":
            print("\n💰 CHARGE TOKEN")
            token = input("Enter token: ").strip()
            
            if not token:
                print("❌ Error: Token cannot be empty")
                continue
                
            amount = input("Enter amount (e.g., 49.99): ").strip()
            
            if not amount:
                print("❌ Error: Amount cannot be empty")
                continue
                
            try:
                float_amount = float(amount)
                if float_amount <= 0:
                    print("❌ Error: Amount must be positive")
                    continue
            except ValueError:
                print("❌ Error: Invalid amount format")
                continue
                
            print(f"🔄 Processing charge of ${amount}...")
            response = request_charge(token, amount)
            if response:
                print(f"✅ {response}")
                print(f"💸 Amount charged: ${amount}")
                print(f"🎫 Token used: {token}")
            else:
                print("❌ Charge failed - check token and try again")

        elif choice == "0":
            print("\n👋 Thanks for using the PCI-DSS Tokenization System!")
            print("🛡️  Remember: This is for educational purposes only")
            break
            
        else:
            print("❌ Invalid choice. Please select 0, 1, 2, or 3.")

def test_server_connection():
    """Test if the tokenization server is running"""
    import requests
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            print("✅ Server connection successful")
            return True
        else:
            print(f"⚠️  Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print("💡 Make sure the FastAPI server is running on http://localhost:8000")
        return False

if __name__ == "__main__":
    print("🔄 Testing server connection...")
    if test_server_connection():
        main()
    else:
        print("\n🚨 Server not available. Please start the server first:")
        print("   uvicorn token_server.main:app --reload")
        sys.exit(1)
