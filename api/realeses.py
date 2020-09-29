from fastapi import APIRouter, Query
from starlette.responses import JSONResponse
from api.api_types import ReleaseWithArtistMeta
from api.database.db_release import release_dict

releases = APIRouter()


@releases.get('/stream/releases/{release_id}', response_model=ReleaseWithArtistMeta)
async def get_release(release_id: int = Query(None, ge=1, le=1000000000)) -> ReleaseWithArtistMeta or JSONResponse:
    if release := await release_dict(release_id=release_id, prefix=False):
        return release
    else:
        return JSONResponse(status_code=404, content={"error": "release {} not found".format(release_id)})
