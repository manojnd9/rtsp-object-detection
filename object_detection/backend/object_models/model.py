from ultralytics import YOLO

Model = YOLO("yolov8n.pt")


class ObjectDetector:

    def __init__(self, model=YOLO, model_path="yolov8n.pt"):
        self.model = model(model_path)

    def detect(self, frame):
        out = self.model.predict(frame)
        return out
