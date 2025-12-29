from fastapi import Header, HTTPException
from app.db.session import SessionLocal
from app.db.models import SDKCommand
import sqlite3, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "labguard.db")


def verify_sdk_key(x_api_key: str = Header(...)):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "SELECT api_key FROM sdk_keys WHERE api_key=? AND active=1",
        (x_api_key,)
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=401, detail="Invalid SDK key")

    return True
