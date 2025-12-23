import os
import cv2
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAPSHOT_ROOT = os.path.join(BASE_DIR, "storage", "snapshots")


def save_snapshot(frame, user_id: str):
    """
    Saves snapshot with timestamp
    Returns saved file path
    """

    date_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H-%M-%S")

    folder = os.path.join(SNAPSHOT_ROOT, date_str)
    os.makedirs(folder, exist_ok=True)

    filename = f"{user_id}_{time_str}.jpg"
    path = os.path.join(folder, filename)

    cv2.imwrite(path, frame)

    return path
