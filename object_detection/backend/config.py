from dataclasses import dataclass

from ultralytics import YOLO


@dataclass
class ModelSelector:
    model: type = YOLO
    path: str = "yolov8n.pt"
