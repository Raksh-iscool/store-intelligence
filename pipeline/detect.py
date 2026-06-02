from ultralytics import YOLO
import cv2

VIDEO = "data/videos/CAM 5.mp4"

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(VIDEO)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model(
        frame,
        classes=[0],
        verbose=False
    )

    annotated = results[0].plot()

    cv2.imshow(
        "YOLO Detection",
        annotated
    )

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()