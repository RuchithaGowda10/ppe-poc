from fastapi import APIRouter, Depends
from app.db.session import SessionLocal
from app.db.models import SDKCommand, EntryLog
from app.auth.sdk_auth import verify_sdk_key
import json
import base64
import cv2
import numpy as np

router = APIRouter()


def decode_frame(b64):
    img = base64.b64decode(b64)
    arr = np.frombuffer(img, dtype=np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


@router.post("/ingest")
def ingest(data: dict, _=Depends(verify_sdk_key)):
    db = SessionLocal()

    cmd = db.query(SDKCommand).get(data["command_id"])
    if not cmd:
        return {"status": "INVALID_COMMAND"}

    frame = decode_frame(data["frames"][0])

    # 🔴 PLACEHOLDER PPE LOGIC
    compliant = False  # replace with real model later

    cmd.status = "DONE"
    cmd.result = json.dumps({"compliant": compliant})

    payload = json.loads(cmd.payload)

    entry = EntryLog(
        user_id=payload["user_id"],
        lab_id=cmd.lab_id,
        compliant=compliant
    )

    db.add(entry)
    db.commit()
    db.close()

    return {"status": "OK"}
