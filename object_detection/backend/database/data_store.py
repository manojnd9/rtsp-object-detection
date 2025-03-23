from object_detection.backend.database.data_model import StrmSessions
from object_detection.backend.database.db_utils import get_db_session
from object_detection.backend.database.schema import StreamSession


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
        )
        db.add(session_row)
        db.commit()
