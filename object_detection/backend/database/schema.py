from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class BoundingBox(BaseModel):
    """A bounding box has xyxy values that define four corners"""

    x1: float
    y1: float
    x2: float
    y2: float


class DetectionResult(BaseModel):
    """Each detected object as a box has:
    - timestamp: at which the object was detected
    - label: name of of the object
    - confidence: confidence of detected objected by the model
    - bbox: bounding box coordinates
    - frame_path: path where input frame is stored
    """

    timestamp: datetime
    label: str
    confidence: float
    bbox: BoundingBox
    frame_path: str
    session_id: UUID


class StreamSession(BaseModel):
    """Global session schema to help partion the
    way frames and detection results are stored.
    """

    year: int
    month: int
    day: int
    session_id: UUID
    stream_name: str
    device_name: str
    device_id: str
