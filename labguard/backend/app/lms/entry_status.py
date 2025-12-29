from fastapi import APIRouter
import sqlite3, os, json

router = APIRouter()

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
DB_PATH = os.path.join(BASE_DIR, "labguard.db")


@router.get("/entry-status")
def entry_status(lab_id: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1️⃣ Check latest entry result
    cur.execute("""
        SELECT compliant, detected_ppe, missing_ppe, snapshot_path
        FROM entry_results
        WHERE lab_id = ?
        ORDER BY created_at DESC
        LIMIT 1
    """, (lab_id,))

    row = cur.fetchone()

    if not row:
        conn.close()
        return {
            "status": "WAITING"
        }

    compliant, detected_ppe, missing_ppe, snapshot = row

    conn.close()

    return {
        "status": "ALLOW" if compliant else "BLOCK",
        "detected_ppe": json.loads(detected_ppe),
        "missing_ppe": json.loads(missing_ppe),
        "snapshot_url": snapshot
    }
