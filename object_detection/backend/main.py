from dotenv import load_dotenv
import os

from object_detection.backend.config import MiscConfig, ModelSelector
from object_detection.backend.object_models.model import ObjectDetector
from object_detection.backend.rtsp.video_stream import video_stream_process
from object_detection.backend.utils.utils import get_stream_session, pre_stream_check
from object_detection.backend.database.data_model import Base
from object_detection.backend.database.data_engine import engine


def main():
    # Load env
    load_dotenv(dotenv_path="object_detection/backend/.env")
    stream_url = os.getenv("RTSP_STREAM_URL")

    # Pre-Stream Connection Check
    if not pre_stream_check(stream_url):
        raise ConnectionError(f"Unable to connect to {stream_url}")
    # Load model info
    model = ModelSelector()

    if not model.model and not model.path:
        raise ValueError("Object Model and Path to .pt file missing!")

    detector = ObjectDetector(model=model.model, model_path=model.path)

    # Define current session_id
    stream_session = get_stream_session()

    misc_config = MiscConfig()

    # Check and set up db tables
    Base.metadata.create_all(bind=engine)

    # Call video stream process function
    video_stream_process(
        stream_url=stream_url,
        stream_session=stream_session,
        object_detector=detector,
        sampling_rate=misc_config.sampling_rate,
        viz=misc_config.opencv_visualisation,
    )


if __name__ == "__main__":
    main()
