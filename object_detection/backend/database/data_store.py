from datetime import datetime, timezone

from object_detection.backend.config import ModelSelector
from object_detection.backend.database.data_model import Detections, StrmSessions
from object_detection.backend.database.db_utils import get_db_session
from object_detection.backend.database.schema import DetectionResult, StreamSession


def store_stream_session(session: StreamSession) -> None:
    # Check for empty session
    if not session:
        raise ValueError("Empty stream session")
    with get_db_session() as db:
        session_row = StrmSessions(
            session_id=session.session_id,
            year=session.year,
            month=session.month,
            day=session.day,
            stream_name=session.stream_name,
            device_name=session.device_name,
            device_id=session.device_id,
            detect_model_name=ModelSelector.name_meta,
            detect_model_version=ModelSelector.path,
            stream_start=datetime.now(timezone.utc),
            stream_end=None,
        )
        if not session_row:
            raise ValueError("Invalid session data!")
        db.add(session_row)
        db.commit()


def store_object_detection_result(detection: DetectionResult) -> None:
    if not detection:
        raise ValueError("Empty detection! Cannot be inserted into the db")

    with get_db_session() as db:
        detect_row = Detections(
            timestamp=detection.timestamp,
            label=detection.label,
            confidence=detection.confidence,
            frame_path=detection.frame_path,
            x1=detection.bbox.x1,
            y1=detection.bbox.y1,
            x2=detection.bbox.x2,
            y2=detection.bbox.y2,
            session_id=detection.session_id,
        )
        if not detect_row:
            raise ValueError("Invlaid detection data!")
        db.add(detect_row)
        db.commit()
