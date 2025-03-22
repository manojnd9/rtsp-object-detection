from datetime import datetime, timezone
import cv2 as cv
from pathlib import Path
import os

from object_detection.backend.database.schema import StreamSession


def save_frame(
    stream_session: StreamSession, timestamp: datetime, frame: cv.typing.MatLike
):
    """Save the running frame along with the timestamp within file name
    as jpg file.
    For now, the frames are stored in the local disk, for later it can
    be pushed to s3 buckets with proper partitioning.
    """

    f_name = f"frame_{timestamp.strftime('%Y%m%d_%H%M%S_%f')}.jpg"
    f_dir = Path(
        "./object_detection/backend/data/streamed_data",
        stream_session.year,
        stream_session.month,
        stream_session.day,
        stream_session.session_id,
    )
    f_path = Path(f_dir, f_name)

    if not os.path.exists(f_dir):
        os.makedirs(f_dir)

    cv.imwrite(f_path, frame)
    return f_path


def get_session_id():
    """
    Based on current timestamp and session schema
    generate and return session schema object.
    """
    timestamp = datetime.now(timezone.utc)

    stream_session = StreamSession(
        year=f"{timestamp.strftime('%Y')}",
        month=f"{timestamp.strftime('%m')}",
        day=f"{timestamp.strftime('%d')}",
        session_id=f"{timestamp.strftime('%Y%m%d_%H%M%S')}",
    )

    return stream_session
