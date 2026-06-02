from ultralytics import YOLO
import cv2

VIDEO = "data/videos/CAM 3.mp4"

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(VIDEO)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model.track(
    frame,
    persist=True,
    tracker="bytetrack.yaml",
    classes=[0],
    conf=0.25,
    iou=0.5,
    verbose=False
)
    

    annotated = results[0].plot()

    cv2.imshow(
        "Tracking",
        annotated
    )
    if results[0].boxes.id is not None:
        ids = results[0].boxes.id.cpu().numpy().astype(int)
        print("Tracked IDs:", ids)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()