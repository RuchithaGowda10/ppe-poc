import os
import cv2
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SNAPSHOT_ROOT = os.path.join(BASE_DIR, "storage", "snapshots")

def save_snapshot(frame, lab_id: str, user_id: str):
    """
    Saves snapshot with timestamp
    Returns relative URL path
    """

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H-%M-%S")

    folder = os.path.join(SNAPSHOT_ROOT, lab_id, date_str)
    os.makedirs(folder, exist_ok=True)

    filename = f"{user_id}_{time_str}.jpg"
    path = os.path.join(folder, filename)

    cv2.imwrite(path, frame)

    # return URL path (frontend/email friendly)
    return f"/snapshots/{lab_id}/{date_str}/{filename}"
