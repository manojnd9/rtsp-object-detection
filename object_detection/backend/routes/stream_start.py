from fastapi import APIRouter, BackgroundTasks
from starlette import status
from pydantic import BaseModel, AnyUrl
from typing import Optional

from object_detection.backend.rtsp.video_stream import video_stream_process
from object_detection.backend.utils.runtime import check_stream, select_model
from object_detection.backend.utils.utils import get_stream_session


class SteamRequestParams(BaseModel):
    stream_url: AnyUrl
    steam_name: str
    device_name: Optional[str] = None
    device_id: Optional[str] = None
    sampling_rate: Optional[int] = 30


router = APIRouter(prefix="/stream", tags=["Streaming"])


@router.post("/start", status_code=status.HTTP_200_OK)
async def start_stream_process(
    stream_request: SteamRequestParams, background_tasks: BackgroundTasks
):
    print(stream_request)
    check_stream(stream_url=str(stream_request.stream_url))
    detector = select_model()

    # stream session metadata
    stream_session = get_stream_session()

    background_tasks.add_task(
        video_stream_process,
        str(stream_request.stream_url),
        stream_session,
        detector,
        stream_request.sampling_rate,
    )

    return {"message": "stream started"}
