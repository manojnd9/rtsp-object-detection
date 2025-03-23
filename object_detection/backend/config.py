from dataclasses import dataclass

from ultralytics import YOLO


@dataclass
class ModelSelector:
    model: type = YOLO
    path: str = "yolov8n.pt"
    name_meta: str = "YOLO"


@dataclass
class MiscConfig:
    """Miscellaneous config"""

    sampling_rate: int = 30
    opencv_visualisation: bool = False
