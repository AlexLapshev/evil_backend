from fastapi import APIRouter, Query
from starlette.responses import JSONResponse
from typing import List

from api.api_types import ArtistMeta, ArtistxReleasesMeta, ReleaseWithArtistMeta
from api.database.db_artists import artist_releases_dict, artist_tracks_dict, get_artist
from api.database.models import Artist

artists = APIRouter()


@artists.get('/artists')
async def all_artists():
    all = await Artist.query.gino.all()
    all = [artist.to_dict() for artist in all]
    return all


@artists.get('/artists/{artist_id}')
async def artist(artist_id: int = Query(None, ge=1, le=1000000000)) -> ArtistMeta or JSONResponse:
    if ar := await get_artist(artist_id=artist_id):
        return ar.to_dict()
    else:
        return JSONResponse(status_code=404, content={"error": "not found"})


@artists.get('/artists/{artist_id}/releases', response_model=ArtistxReleasesMeta)
async def get_artists_releases(artist_id: int = Query(None, ge=1, le=1000000000)) \
        -> ArtistxReleasesMeta or JSONResponse:
    if artist_release := await artist_releases_dict(artist_id=artist_id):
        return artist_release
    else:
        return JSONResponse(status_code=404, content={"error": "not found"})


@artists.get('/artists/tracks/{artist_id}', response_model=ArtistMeta)
async def get_artists_track(artist_id: int = Query(None, ge=1, le=1000000000)) -> ArtistMeta or JSONResponse:
    if artist_track := await artist_tracks_dict(artist_id=artist_id):
        return artist_track
    else:
        return JSONResponse(status_code=404, content={"error": "not found"})
