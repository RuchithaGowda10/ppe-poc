from fastapi import APIRouter
from app.db.session import SessionLocal
from app.db.models import SDKCommand
import json

router = APIRouter()


@router.get("/entry-result")
def entry_result(request_id: int):
    db = SessionLocal()
    cmd = db.query(SDKCommand).get(request_id)

    if not cmd or cmd.status != "DONE":
        db.close()
        return {"processing": True}

    result = json.loads(cmd.result)
    db.close()

    return {"compliant": result["compliant"]}
