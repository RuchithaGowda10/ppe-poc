import cv2

RTSP_URL = "rtsp://admin:atomwalk%4011@192.168.0.60:554/stream1"

def capture_frame():
    cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)

    if not cap.isOpened():
        raise RuntimeError("Failed to open RTSP stream")

    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise RuntimeError("Failed to read frame from camera")

    return frame
