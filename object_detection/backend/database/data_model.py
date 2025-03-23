from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP
import uuid
import datetime

from object_detection.backend.database.data_engine import Base


class StrmSessions(Base):
    __tablename__ = "stream_sessions"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), unique=True, nullable=False
    )
    year: Mapped[int] = mapped_column(nullable=False)
    month: Mapped[int] = mapped_column(nullable=False)
    day: Mapped[int] = mapped_column(nullable=False)
    stream_name: Mapped[str] = mapped_column(nullable=True)
    device_name: Mapped[str] = mapped_column(nullable=True)
    device_id: Mapped[str] = mapped_column(nullable=True)
    detect_model_name: Mapped[str] = mapped_column(nullable=True)
    detect_model_version: Mapped[str] = mapped_column(nullable=True)
    stream_start: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    stream_end: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )

    # A session with many detections
    detections: Mapped[list["Detections"]] = relationship(back_populates="session")


class Detections(Base):
    __tablename__ = "detections"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    label: Mapped[str] = mapped_column(nullable=False)
    confidence: Mapped[float] = mapped_column(nullable=False)
    frame_path: Mapped[str] = mapped_column(nullable=False)

    x1: Mapped[float] = mapped_column(nullable=False)
    y1: Mapped[float] = mapped_column(nullable=False)
    x2: Mapped[float] = mapped_column(nullable=False)
    y2: Mapped[float] = mapped_column(nullable=False)

    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("stream_sessions.session_id"), nullable=False
    )

    # Detections belonging to unique session
    session: Mapped["StrmSessions"] = relationship(back_populates="detections")
