
#!/bin/bash

echo "🔄 Starting PCI-DSS Tokenization System..."

# Activate virtual environment
echo "🧪 Activating Python virtual environment..."
source venv/bin/activate || source venv/Scripts/activate

# Load env
export $(grep -v '^#' .env | xargs)

# Check required files
mkdir -p data
touch data/audit.log
touch data/purchases.json
if [ ! -f data/token_map.json ]; then
  echo "{}" > data/token_map.json
fi

# Start the FastAPI server
echo "🚀 Starting Tokenization Server (FastAPI)..."
uvicorn token_server.main:app --reload &
SERVER_PID=$!

# Wait a moment for the server to start
sleep 2

# Run the CLI app
echo "💻 Starting Merchant CLI..."
python merchant_cli/cli.py

# After CLI ends, kill the server
echo "🛑 Shutting down server..."
kill $SERVER_PID

echo "✅ System stopped."
