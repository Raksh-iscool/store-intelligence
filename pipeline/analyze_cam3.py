from ultralytics import YOLO
import cv2

VIDEO = "data/videos/CAM 3.mp4"

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(VIDEO)

frame_count = 0

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1

    if frame_count % 150 != 0:
        continue

    results = model(frame, classes=[0], verbose=False)

    people = len(results[0].boxes)

    print(
        f"Frame {frame_count}: "
        f"{people} people"
    )

cap.release()