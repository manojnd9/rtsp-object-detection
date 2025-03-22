from dotenv import load_dotenv
import os

from object_detection.backend.config import ModelSelector
from object_detection.backend.object_models.model import ObjectDetector
from object_detection.backend.rtsp.video_stream import video_stream_process
from object_detection.backend.utils.save_frame import get_session_id


def main():
    # Load env
    load_dotenv(dotenv_path="object_detection/backend/.env")
    stream_url = os.getenv("RTSP_STREAM_URL")

    # Load model info
    model = ModelSelector()

    if not model.model and not model.path:
        raise ValueError("Object Model and Path to .pt file missing!")

    detector = ObjectDetector(model=model.model, model_path=model.path)

    # Define current session_id
    stream_session = get_session_id()

    # Sampling rate
    sampling_rate = 3

    # Call video stream process function
    video_stream_process(
        stream_url=stream_url,
        stream_session=stream_session,
        object_detector=detector,
        sampling_rate=sampling_rate,
    )


if __name__ == "__main__":
    main()
