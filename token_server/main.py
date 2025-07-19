from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from token_server.auth import is_authorized
from token_server.token_logic import generate_token
from token_server.vault import encrypt_pan, store_mapping, get_encrypted_pan, decrypt_pan, record_purchase
from token_server.logger import log

app = FastAPI(title="PCI-DSS Tokenization System", description="Educational tokenization service")

class TokenizeRequest(BaseModel):
    pan: str  # Primary Account Number

class DetokenizeRequest(BaseModel):
    token: str

class ChargeRequest(BaseModel):
    token: str
    amount: str

@app.get("/")
async def root():
    return {"message": "PCI-DSS Tokenization Server is running!", "endpoints": ["/tokenize", "/detokenize", "/charge"]}

@app.post("/tokenize")
async def tokenize(request: Request, body: TokenizeRequest):
    """Convert a PAN (card number) into a secure token"""
    try:
        # Check authentication
        auth_header = request.headers.get("Authorization")
        if not is_authorized(auth_header):
            log("UNAUTHORIZED /tokenize", auth_header or "No Header")
            raise HTTPException(status_code=401, detail="Unauthorized")

        # Validate PAN (basic check)
        pan = body.pan.strip()
        if not pan or not pan.isdigit() or len(pan) < 13 or len(pan) > 19:
            log("INVALID_PAN", f"Invalid PAN format: {len(pan)} digits")
            raise HTTPException(status_code=400, detail="Invalid PAN format")

        # Generate token and encrypt PAN
        token = generate_token()
        encrypted = encrypt_pan(pan)
        store_mapping(token, encrypted)
        
        log("TOKENIZED", f"{token}")
        return {"token": token, "message": "PAN successfully tokenized"}
        
    except HTTPException:
        raise
    except Exception as e:
        log("TOKENIZE_ERROR", str(e))
        raise HTTPException(status_code=500, detail="Internal server error during tokenization")

@app.post("/detokenize")
async def detokenize(request: Request, body: DetokenizeRequest):
    """Convert a token back to the original PAN"""
    try:
        # Check authentication
        auth_header = request.headers.get("Authorization")
        if not is_authorized(auth_header):
            log("UNAUTHORIZED /detokenize", auth_header or "No Header")
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = body.token.strip()
        if not token:
            raise HTTPException(status_code=400, detail="Token is required")

        # Get encrypted PAN
        encrypted_pan = get_encrypted_pan(token)
        if not encrypted_pan:
            log("DETOKENIZE_FAILED", f"Token not found: {token}")
            raise HTTPException(status_code=404, detail="Token not found")
        
        # Decrypt PAN
        pan = decrypt_pan(encrypted_pan)
        log("DETOKENIZED", f"{token}")
        return {"pan": pan, "message": "Token successfully detokenized"}
        
    except HTTPException:
        raise
    except Exception as e:
        log("DETOKENIZE_ERROR", f"Decryption failed for {body.token}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during detokenization")

@app.post("/charge")
async def charge(request: Request, body: ChargeRequest):
    """Process a charge against a token"""
    try:
        # Check authentication
        auth_header = request.headers.get("Authorization")
        if not is_authorized(auth_header):
            log("UNAUTHORIZED /charge", auth_header or "No Header")
            raise HTTPException(status_code=401, detail="Unauthorized")

        token = body.token.strip()
        amount = body.amount.strip()
        
        # Validate inputs
        if not token:
            raise HTTPException(status_code=400, detail="Token is required")
        if not amount:
            raise HTTPException(status_code=400, detail="Amount is required")
        
        # Validate amount format
        try:
            float_amount = float(amount)
            if float_amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid amount format")
        
        # Verify token exists (this also validates the token)
        encrypted_pan = get_encrypted_pan(token)
        if not encrypted_pan:
            log("CHARGE_FAILED", f"Token not found: {token}")
            raise HTTPException(status_code=404, detail="Token not found")
        
        # Record the purchase (in real world, this would process the payment)
        record_purchase(token, amount)
        log("CHARGED", f"{token} - Amount: ${amount}")
        
        return {
            "message": f"Successfully charged ${amount} to token {token}",
            "token": token,
            "amount": amount,
            "status": "success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        log("CHARGE_ERROR", f"Charge failed for {body.token}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during charge")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "tokenization-server"}
