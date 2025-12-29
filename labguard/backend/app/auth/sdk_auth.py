import sqlite3
from fastapi import Header, HTTPException

DB_PATH = "labguard.db"

def verify_sdk_key(authorization: str = Header(...)):
    # Expect: Authorization: Bearer <API_KEY>
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")

    api_key = authorization.replace("Bearer ", "").strip()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT lab_id, sdk_id, active
        FROM sdk_keys
        WHERE api_key = ?
    """, (api_key,))

    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=401, detail="Invalid API key")

    lab_id, sdk_id, active = row

    if not active:
        raise HTTPException(status_code=403, detail="SDK key revoked")

    return {
        "lab_id": lab_id,
        "sdk_id": sdk_id
    }
