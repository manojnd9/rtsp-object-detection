from pydantic import BaseModel
from datetime import datetime

"""A bounding box has xyxy values that define four corners"""


class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


"""Each detected object as a box has:
    - timestamp: at which the object was detected
    - label: name of of the object
    - confidence: confidence of detected objected by the model
    - bbox: bounding box coordinates
    - frame_path: path where input frame is stored
"""


class DetectionResult(BaseModel):
    timestamp: datetime
    label: str
    confidence: float
    bbox: BoundingBox
    frame_path: str
