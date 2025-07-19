import os
from dotenv import load_dotenv

load_dotenv()
EXPECTED_TOKEN = os.getenv("AUTH_TOKEN")

def is_authorized(header_value: str) -> bool:
    if not header_value:
        return False

    scheme, _, token = header_value.partition(" ")
    return scheme.lower() == "bearer" and token == EXPECTED_TOKEN
