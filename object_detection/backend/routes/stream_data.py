from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from object_detection.backend.database.data_model import StrmSessions
from object_detection.backend.database.data_engine import SessionLocal


router = APIRouter(prefix="/session_data", tags=["Streaming Data"])


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Dependency injection
session_db_dependency = Annotated[Session, Depends(get_db)]

# Last 10 session_ids with all the details


@router.get("/sessions")
async def get_recent_sessions(db: session_db_dependency):
    sessions = (
        db.query(StrmSessions)
        .order_by(StrmSessions.stream_start.desc())
        .limit(10)
        .all()
    )
    return sessions


# Download the session detection data as parquet along with the frames
