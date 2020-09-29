from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from starlette.responses import JSONResponse
import os

from api.api_types import TrackFullMeta
from api.database.db_track import select_track, track_do_dict

tracks = APIRouter()


@tracks.get('/metadata/tracks/{track_id}', response_model=TrackFullMeta)
async def get_track(track_id: int = Query(None, ge=1, le=1000000000)) -> TrackFullMeta or JSONResponse:
    if track := await select_track(track_id=track_id):
        return await track_do_dict(track, False)
    else:
        return JSONResponse(status_code=404, content={"error": "not found"})


filepath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../media/01_gospel_for_a_new_century.flac'))


@tracks.get('/stream/tracks/')
async def stream_track() -> StreamingResponse:
    file = open(filepath, mode="rb")
    return StreamingResponse(file, media_type="audio/flac")
