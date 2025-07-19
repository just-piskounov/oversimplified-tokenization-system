from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from token_server.auth import is_authorized
from token_server.token_logic import generate_token
from token_server.vault import encrypt_pan, store_mapping
from token_server.logger import log

app = FastAPI()

class TokenizeRequest(BaseModel):
    pan: str  # Primary Account Number

@app.post("/tokenize")
async def tokenize(request: Request, body: TokenizeRequest):
    auth_header = request.headers.get("Authorization")
    if not is_authorized(auth_header):
        log("UNAUTHORIZED /tokenize", auth_header or "No Header")
        raise HTTPException(status_code=401, detail="Unauthorized")

    pan = body.pan
    token = generate_token()
    encrypted = encrypt_pan(pan)
    store_mapping(token, encrypted)
    log("TOKENIZED", f"{token}")
    return {"token": token}

