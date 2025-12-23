from fastapi import APIRouter, HTTPException, Depends
from app.ai.rtsp_reader import capture_frame
from app.ai.ppe_detector import PPEDetector
from app.auth.dependencies import get_current_user
from app.utils.snapshot import save_snapshot
from app.ai.decision_engine import DecisionEngine
import os

router = APIRouter()

def get_ppe_detector():
    return PPEDetector()

def get_decision_engine():
    return DecisionEngine()

@router.post("/trigger-entry")
def trigger_entry(
    lab_id: str,
    current_user: str = Depends(get_current_user)
):
    try:
        # 1️⃣ Capture frame
        frame = capture_frame()
        if frame is None:
            raise HTTPException(status_code=500, detail="Camera frame not captured")

        # 2️⃣ Detect person + PPE
        detection, annotated = ppe_detector.detect(frame)

        # 3️⃣ Save snapshot
        snapshot_path = save_snapshot(annotated, current_user, lab_id)
        snapshot_filename = os.path.basename(snapshot_path)
        snapshot_url = f"/snapshots/{lab_id}/{snapshot_filename}"

        # 4️⃣ No person at door
        if not detection["person_detected"]:
            return {
                "status": "NO_PERSON",
                "lab_id": lab_id,
                "snapshot_url": snapshot_url
            }

        # 5️⃣ Decision
        decision = decision_engine.evaluate(
            lab_id=lab_id,
            detected_ppe=detection["ppe_detected"]
        )

        # 6️⃣ Final response (ERP-ready)
        return {
            "status": "COMPLIANT" if decision["compliant"] else "BLOCK",
            "user_id": current_user,
            "lab_id": lab_id,
            "ppe_compliant": decision["compliant"],
            "detected_ppe": decision["detected_ppe"],
            "required_ppe": decision["required_ppe"],
            "missing_ppe": decision["missing_ppe"],
            "snapshot_url": snapshot_url
        }

    except Exception as e:
        print("Trigger error:", e)
        raise HTTPException(status_code=500, detail="Trigger processing failed")
