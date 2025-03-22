from datetime import datetime, timezone
import cv2 as cv
from ultralytics import YOLO

from object_detection.backend.database.schema import (
    BoundingBox,
    DetectionResult,
    StreamSession,
)
from object_detection.backend.object_models.model import Model, ObjectDetector
from object_detection.backend.utils.utils import save_frame


def video_stream_process(
    stream_url: str,
    stream_session: StreamSession,
    object_detector: ObjectDetector,
    sampling_rate: int = 30,
    viz: bool = False,
) -> None:
    # Object Detector
    detector = object_detector

    # Capture object
    cap = cv.VideoCapture(stream_url)

    # frame counter with sampling
    frame_counter = 0

    if not cap.isOpened():
        raise ValueError("No stream or video available")

    while cap.isOpened():
        # Capture each frame
        retval, frame = cap.read()
        # return is true if there is frame/image read
        if not retval:
            break

        # Sampling
        frame_counter += 1
        if frame_counter % sampling_rate != 0:
            continue

        # Call the object model detecting function
        results = detector.detect(frame=frame)

        # Since in each call one image/frame is processed
        result = results[0]

        # Process each box detected
        boxes = result.boxes.cpu().numpy()

        # Store frame
        timestamp = datetime.now(timezone.utc)
        frame_path = save_frame(stream_session, timestamp, frame)

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

        if viz:
            cv.imshow("Frame", results[0].plot())
            cv.waitKey(1)
            if 0xFF == ord("q"):
                break

    # Release video capture object
    cap.release()

    # Close all frames
    cv.destroyAllWindows()
