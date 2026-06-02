from ultralytics import YOLO
import cv2

VIDEO = "data/videos/CAM 3.mp4"

LINE_X = 900

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(VIDEO)

track_history = {}
FRAME_SKIP = 5
frame_count = 0

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

    cv2.line(
        frame,
        (LINE_X, 0),
        (LINE_X, frame.shape[0]),
        (0, 0, 255),
        2
    )

    if (
        results[0].boxes.id is not None
        and len(results[0].boxes) > 0
    ):

        ids = results[0].boxes.id.cpu().numpy().astype(int)

        boxes = results[0].boxes.xyxy.cpu().numpy()

        for track_id, box in zip(ids, boxes):

            x1, y1, x2, y2 = box

            center_x = int((x1 + x2) / 2)

            if track_id not in track_history:
                track_history[track_id] = center_x
                continue

            previous_x = track_history[track_id]

            if previous_x > LINE_X and center_x < LINE_X:
                print(
                    f"ENTRY : VIS_{track_id}"
                )

            elif previous_x < LINE_X and center_x > LINE_X:
                print(
                    f"EXIT : VIS_{track_id}"
                )

            track_history[track_id] = center_x

    # cv2.imshow("Events", frame)

    # if cv2.waitKey(1) == 27:
    #     break
    pass

cap.release()
cv2.destroyAllWindows()