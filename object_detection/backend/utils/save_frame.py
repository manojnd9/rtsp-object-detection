from datetime import datetime
import cv2 as cv
from pathlib import Path
import os

"""Save the running frame along with the timestamp within file name
    as jpg file.
    For now, the frames are stored in the local disk, for later it can
    be pushed to s3 buckets with proper partitioning.
"""


def save_frame(timestamp: datetime, frame: cv.typing.MatLike):
    f_name = f"frame_{timestamp.strftime('%Y%m%d_%H%M%S_%f')}.jpg"
    f_dir = Path("./object_detection/backend/data/streamed_data")
    f_path = Path("./object_detection/backend/data/streamed_data", f_name)

    if not os.path.exists(f_dir):
        os.makedirs(f_dir)

    cv.imwrite(f_path, frame)
    return f_path
