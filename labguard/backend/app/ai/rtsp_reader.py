from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Lab
import cv2

def capture_frame(lab_id: str):
    db: Session = SessionLocal()

    lab = db.query(Lab).filter(Lab.lab_id == lab_id).first()
    if not lab:
        raise RuntimeError("Lab not configured")

    cap = cv2.VideoCapture(lab.rtsp_url, cv2.CAP_FFMPEG)

    if not cap.isOpened():
        raise RuntimeError("Failed to open RTSP")

    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise RuntimeError("Failed to read frame")

    return frame
