import sqlite3, json, time
from fastapi import APIRouter, Depends
from app.auth.sdk_auth import verify_sdk_key
import os

router = APIRouter()

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
DB_PATH = os.path.join(BASE_DIR, "labguard.db")

@router.get("/sdk/commands")
def get_commands(sdk=Depends(verify_sdk_key)):
    lab_id = sdk["lab_id"]

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    timeout = 30
    start = time.time()

    while time.time() - start < timeout:
        cur.execute("""
            SELECT id, command, payload
            FROM sdk_commands
            WHERE lab_id = ?
              AND status = 'PENDING'
            ORDER BY created_at ASC
            LIMIT 1
        """, (lab_id,))

        row = cur.fetchone()
        if row:
            cmd_id, command, payload = row

            cur.execute("""
                UPDATE sdk_commands
                SET status = 'SENT'
                WHERE id = ?
            """, (cmd_id,))
            conn.commit()
            conn.close()

            return {
                "command": command,
                "payload": json.loads(payload) if payload else {}
            }

        time.sleep(0.3)

    conn.close()
    return {"command": "NONE"}
