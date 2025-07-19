from datetime import datetime

def log(event: str, detail: str=""):
    with open("data/audit.log", "a") as f:
        f.write(f"{datetime.utcnow().isoformat()} - {event} - {detail}\n")
