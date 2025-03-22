from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv("object_detection/backend/.env")

# Grab database url
database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL missing in environment")


engine = create_engine(database_url, echo=True)
"""Engine to connect the database session.
"""

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
"""Local Session that creates a DB in connection to the Engine that kind off gives a location on the network
where this DB exists.
"""


class Base(DeclarativeBase):
    """creates an object for the DB, which will be used to control the transactions with that DB"""

    pass
