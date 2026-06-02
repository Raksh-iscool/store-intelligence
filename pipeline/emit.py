from ultralytics import YOLO
import cv2
from datetime import datetime
import requests

VIDEO = "data/videos/CAM 5.mp4"

QUEUE_X1 = 850
QUEUE_Y1 = 100

QUEUE_X2 = 1450
QUEUE_Y2 = 1050

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(VIDEO)

seen_ids = set()

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        classes=[0],
        verbose=False
    )

    if results[0].boxes.id is None:
        continue

    ids = results[0].boxes.id.cpu().numpy().astype(int)
    boxes = results[0].boxes.xyxy.cpu().numpy()

    for track_id, box in zip(ids, boxes):

        x1, y1, x2, y2 = box

        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)

        inside_queue = (
            QUEUE_X1 <= cx <= QUEUE_X2
            and
            QUEUE_Y1 <= cy <= QUEUE_Y2
        )

        if inside_queue and track_id not in seen_ids:

            seen_ids.add(track_id)

            event = {
                "event_id": f"queue_{track_id}",
                "store_id": "STORE_BLR_001",
                "camera_id": "CAM_5",
                "visitor_id": f"VIS_{track_id}",
                "event_type": "BILLING_QUEUE_JOIN",
                "timestamp": datetime.utcnow().isoformat(),
                "zone_id": "BILLING",
                "dwell_ms": 0,
                "is_staff": False,
                "confidence": 0.9
            }

            try:

                response = requests.post(
                    "http://127.0.0.1:8000/events/ingest",
                    json={
                        "events": [event]
                    },
                    timeout=5
                )

                print(
                    event["visitor_id"],
                    response.status_code
                )

            except Exception as e:

                print(
                    "POST FAILED:",
                    e
                )

cap.release()