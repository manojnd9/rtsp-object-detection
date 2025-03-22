from dotenv import load_dotenv
import os

from object_detection.backend.config import ModelSelector
from object_detection.backend.object_models.model import ObjectDetector
from object_detection.backend.rtsp.video_stream import video_stream_process


def main():
    # Load env
    load_dotenv(dotenv_path="object_detection/backend/.env")
    stream_url = os.getenv("RTSP_STREAM_URL")

    # Load model info

    model = ModelSelector().model
    model_path = ModelSelector().path

    if not model and not model_path:
        raise ValueError("Object Model and Path to .pt file missing!")

    detector = ObjectDetector(model=model, model_path=model_path)
    # Call video stream process function
    video_stream_process(stream_url=stream_url, object_detector=detector)


if __name__ == "__main__":
    main()
