from contextlib import contextmanager
from sqlalchemy.orm.session import Session

from object_detection.backend.database.data_engine import SessionLocal


@contextmanager
def get_db_session():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
