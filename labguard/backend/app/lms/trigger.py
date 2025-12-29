from fastapi import APIRouter, HTTPException, Depends
import sqlite3, json, os
from app.auth.dependencies import get_current_user

router = APIRouter()

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
DB_PATH = os.path.join(BASE_DIR, "labguard.db")


@router.post("/trigger-entry")
def trigger_entry(
    lab_id: str,
    current_user: str = Depends(get_current_user)
):
    try:
        user_id = current_user

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO sdk_commands (lab_id, command, payload)
            VALUES (?, ?, ?)
        """, (
            lab_id,
            "CAPTURE_ENTRY",
            json.dumps({
                "user_id": user_id,
                "frames": 3,
                "window_sec": 5
            })
        ))

        conn.commit()
        conn.close()

        return {
            "status": "ENTRY_TRIGGERED",
            "lab_id": lab_id,
            "user_id": user_id,
            "message": "Waiting for SDK capture"
        }

    except Exception as e:
        print("Trigger error:", e)
        raise HTTPException(
            status_code=500,
            detail="Failed to trigger entry"
        )
