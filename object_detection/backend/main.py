from dotenv import load_dotenv
import os

from object_detection.backend.config import MiscConfig
from object_detection.backend.rtsp.video_stream import video_stream_process
from object_detection.backend.utils.runtime import check_stream, select_model
from object_detection.backend.utils.utils import get_stream_session
from object_detection.backend.database.data_model import Base
from object_detection.backend.database.data_engine import engine


def main():
    # Check and set up db tables
    Base.metadata.create_all(bind=engine)

    # Load env
    load_dotenv(dotenv_path="object_detection/backend/.env")
    stream_url = os.getenv("RTSP_STREAM_URL")

    if "rtsp" in stream_url:
        check_stream(stream_url)

    detector = select_model()

    # stream session metadata
    stream_session = get_stream_session()

    misc_config = MiscConfig()

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
