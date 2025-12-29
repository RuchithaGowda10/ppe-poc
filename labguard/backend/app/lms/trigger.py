from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import get_current_user
from app.db.session import SessionLocal
from app.db.models import SDKCommand
import json

router = APIRouter()


@router.post("/trigger-entry")
def trigger_entry(
    lab_id: str,
    current_user=Depends(get_current_user)
):
    db = SessionLocal()

    try:
        cmd = SDKCommand(
            sdk_id=f"SDK-{lab_id}",
            lab_id=lab_id,
            command="CAPTURE_ENTRY",
            status="PENDING",
            payload=json.dumps({
                "user_id": current_user["user_id"],
                "frames": 3
            })
        )

        db.add(cmd)
        db.commit()
        db.refresh(cmd)

        return {"request_id": cmd.id}

    except Exception:
        db.rollback()
        raise HTTPException(500, "Trigger failed")

    finally:
        db.close()
