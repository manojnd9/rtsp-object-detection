import cv2 as cv
from ultralytics import YOLO

from object_detection.backend.object_models.model import Model, ObjectDetector

# STREAM_URL = "rtsp://192.168.2.87:8080/h264_ulaw.sdp"
# STREAM_URL = "rtsp://127.0.0.1:8555/downscaled"
STREAM_URL = "video_test.MOV"
# STREAM_URL = "simple-car.jpg"

# Object Detector
detector = ObjectDetector(model=YOLO, model_path="yolov8n.pt")

# Capture object
cap = cv.VideoCapture(STREAM_URL)

if not cap.isOpened():
    raise ValueError("No stream or video available")

while cap.isOpened():
    # Capture each frame
    retval, frame = cap.read()
    # return is true if there is frame/image read
    if not retval:
        break
    results = detector.detect(frame=frame)

    for result in results:
        result.show()
    break
    cv.imshow("Frame", frame)
    cv.waitKey(1)
    if 0xFF == ord("q"):
        break

# Release video capture object
cap.release()

# Close all frames
cv.destroyAllWindows()
