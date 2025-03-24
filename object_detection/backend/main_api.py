from fastapi import FastAPI
from contextlib import asynccontextmanager

from object_detection.backend.routes import stream_start, health, stream_data
from object_detection.backend.database.data_model import Base
from object_detection.backend.database.data_engine import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("app is starting!")
    # Check and set up db tables if they don't exist
    Base.metadata.create_all(bind=engine)
    yield
    print("app is shutting down")


app = FastAPI(
    title="Real-Time Streaming and Object Detection", version="0.0.1", lifespan=lifespan
)


@app.get("/")
async def run_app():
    return "Welcome to RTSP streaming app!"


app.include_router(stream_start.router)
app.include_router(health.router)
app.include_router(stream_data.router)
