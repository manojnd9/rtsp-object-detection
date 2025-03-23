from object_detection.backend.config import ModelSelector
from object_detection.backend.object_models.model import ObjectDetector
from object_detection.backend.utils.utils import pre_stream_check


def check_stream(stream_url: str):
    """Pre-Stream Connection Check"""
    if not pre_stream_check(stream_url):
        raise ConnectionError(f"Unable to connect to {stream_url}")


def select_model() -> ObjectDetector:
    """Select object detection model"""
    model = ModelSelector()

    if not model.model and not model.path:
        raise ValueError("Object Model and Path to .pt file missing!")

    detector = ObjectDetector(model=model.model, model_path=model.path)
    return detector
