import base64, json, sqlite3, os, cv2, numpy as np
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.auth.sdk_auth import verify_sdk_key
from app.ai.ppe_detector import PPEDetector
from app.ai.decision_engine import DecisionEngine
from app.utils.snapshot import save_snapshot

router = APIRouter()
ppe_detector = PPEDetector()
decision_engine = DecisionEngine()

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
DB_PATH = os.path.join(BASE_DIR, "labguard.db")


class SDKIngestPayload(BaseModel):
    sdk_id: str
    frames: list[str]


@router.post("/sdk/ingest")
def ingest_frames(
    payload: SDKIngestPayload,
    sdk=Depends(verify_sdk_key)
):
    lab_id = sdk["lab_id"]

    if not payload.frames:
        raise HTTPException(status_code=400, detail="No frames received")

    # 1️⃣ Decode first frame only
    frame_bytes = base64.b64decode(payload.frames[0])
    np_arr = np.frombuffer(frame_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # 2️⃣ Run PPE detection
    detection, annotated = ppe_detector.detect(frame)

    # 3️⃣ Evaluate compliance
    decision = decision_engine.evaluate(
        lab_id=lab_id,
        detected_ppe=detection["ppe_detected"]
    )

    # 4️⃣ Save snapshot
    snapshot_path = save_snapshot(
        annotated,
        lab_id=lab_id,
        user_id="UNKNOWN"
    )

    # 5️⃣ Store result
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO entry_results (
            lab_id, sdk_id, compliant,
            detected_ppe, missing_ppe, snapshot_path
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        lab_id,
        payload.sdk_id,
        1 if decision["compliant"] else 0,
        json.dumps(decision["detected_ppe"]),
        json.dumps(decision["missing_ppe"]),
        snapshot_path
    ))

    # 6️⃣ Mark command as DONE
    cur.execute("""
        UPDATE sdk_commands
        SET status = 'DONE'
        WHERE lab_id = ?
          AND status = 'SENT'
    """, (lab_id,))

    conn.commit()
    conn.close()

    return {
        "status": "PROCESSED",
        "lab_id": lab_id,
        "compliant": decision["compliant"]
    }
