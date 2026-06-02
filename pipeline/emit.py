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

         response = requests.post(
    "http://127.0.0.1:8000/events/ingest",
    json={
        "events": [event]
    }
)

print(
    event["visitor_id"],
    response.status_code
)   

cap.release()