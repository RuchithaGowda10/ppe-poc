from ultralytics import YOLO
import cv2
import numpy as np

PERSON_MODEL_PATH = "D:\ppe-dl\yolo11n.pt"  
PPE_MODEL_PATH = r"D:\runs\detect\train5\weights\best.pt"  

DOOR_ROI = np.array(
    [
        (566, 3),
        (942, 3),
        (919, 563),
        (562, 594)
    ],
    dtype=np.int32
)


class PPEDetector:
    def __init__(self):
        self.person_model = YOLO(PERSON_MODEL_PATH)
        self.ppe_model = YOLO(PPE_MODEL_PATH)

    def _person_intersects_door(self, x1, y1, x2, y2):
        """
        Check if PERSON bbox center lies inside door ROI
        """
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        return cv2.pointPolygonTest(DOOR_ROI, (cx, cy), False) >= 0

    def detect(self, frame):
        annotated = frame.copy()

        detection_result = {
            "person_detected": False,
            "ppe_detected": []
        }

        person_results = self.person_model(frame, conf=0.5, verbose=False)[0]

        for box in person_results.boxes:
            cls_id = int(box.cls[0])
            label = self.person_model.names[cls_id]

            if label != "person":
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            if not self._person_intersects_door(x1, y1, x2, y2):
                continue

            detection_result["person_detected"] = True

            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                annotated,
                "PERSON",
                (x1, y1 - 6),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            person_crop = frame[y1:y2, x1:x2]
            if person_crop.size == 0:
                break

            ppe_results = self.ppe_model(person_crop, conf=0.25, verbose=False)[0]

            for pbox in ppe_results.boxes:
                ppe_cls = int(pbox.cls[0])
                ppe_label = self.ppe_model.names[ppe_cls]

                if ppe_label not in detection_result["ppe_detected"]:
                    detection_result["ppe_detected"].append(ppe_label)

                px1, py1, px2, py2 = map(int, pbox.xyxy[0])

                cv2.rectangle(
                    annotated,
                    (x1 + px1, y1 + py1),
                    (x1 + px2, y1 + py2),
                    (255, 0, 0),
                    2
                )
                cv2.putText(
                    annotated,
                    ppe_label,
                    (x1 + px1, y1 + py1 - 4),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 0, 0),
                    2
                )

            break

        return detection_result, annotated
