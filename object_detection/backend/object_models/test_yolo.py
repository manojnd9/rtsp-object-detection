from ultralytics import YOLO

import cv2

frame = cv2.imread("simple-car.jpg")

# Load the model
model = YOLO("yolov8n.pt")

if frame is None:
    raise ValueError("Empty or error in frame")


results = model(frame)

for result in results:
    result.show()
