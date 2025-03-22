import cv2 as cv
from ultralytics import YOLO

from object_detection.backend.object_models.model import Model, ObjectDetector


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
