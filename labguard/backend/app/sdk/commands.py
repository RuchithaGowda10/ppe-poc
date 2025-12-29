from fastapi import APIRouter, Depends
from app.db.session import SessionLocal
from app.db.models import SDKCommand
from app.auth.sdk_auth import verify_sdk_key
import json

router = APIRouter()


@router.get("/commands")
def get_commands(lab_id: str, _=Depends(verify_sdk_key)):
    db = SessionLocal()

    cmd = db.query(SDKCommand)\
        .filter_by(lab_id=lab_id, status="PENDING")\
        .first()

    if not cmd:
        db.close()
        return {"command": "IDLE"}

    cmd.status = "IN_PROGRESS"
    db.commit()

    response = {
        "command": cmd.command,
        "command_id": cmd.id,
        "payload": json.loads(cmd.payload)
    }

    db.close()
    return response
