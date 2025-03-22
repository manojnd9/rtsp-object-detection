from datetime import datetime, timezone
import cv2 as cv
from ultralytics import YOLO

from object_detection.backend.database.schema import BoundingBox, DetectionResult
from object_detection.backend.object_models.model import Model, ObjectDetector
from object_detection.backend.utils.save_frame import save_frame


def video_stream_process(stream_url: str, object_detector: ObjectDetector) -> None:
    # Object Detector
    detector = object_detector

    # Capture object
    cap = cv.VideoCapture(stream_url)

    if not cap.isOpened():
        raise ValueError("No stream or video available")

    while cap.isOpened():
        # Capture each frame
        retval, frame = cap.read()
        # return is true if there is frame/image read
        if not retval:
            break
        # Call the object model detecting function
        results = detector.detect(frame=frame)

        # Since in each call one image/frame is processed
        result = results[0]

        # Process each box detected
        boxes = result.boxes.cpu().numpy()

        # Store frame
        timestamp = datetime.now(timezone.utc)
        frame_path = save_frame(timestamp, frame)

        for box in boxes:
            bbox = BoundingBox(
                x1=float(box.xyxy[0][0]),
                y1=float(box.xyxy[0][1]),
                x2=float(box.xyxy[0][2]),
                y2=float(box.xyxy[0][3]),
            )
            detection_data = DetectionResult(
                timestamp=timestamp,
                label=detector.model.names[int(box.cls)],
                confidence=float(box.conf[0]),
                bbox=bbox,
                frame_path=str(frame_path),
            )
        # for xyxy in xyxys:
        #     cv.rectangle(
        #         frame,
        #         (int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])),
        #         (0, 255, 0),
        #     )
        # break
        cv.imshow("Frame", results[0].plot())
        cv.waitKey(1)
        if 0xFF == ord("q"):
            break

    # Release video capture object
    cap.release()

    # Close all frames
    cv.destroyAllWindows()
