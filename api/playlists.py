from fastapi import APIRouter
from typing import List
from starlette.responses import JSONResponse

from api.database.db_playlist import playlist_dict, playlist_update, playlist_delete_from
from api.api_types import PlaylistMeta, PlaylistXTrackMeta
from api.database.models import Playlist
from api.database.db_track import track_do_dict

playlists = APIRouter()


@playlists.get('/playlist/all/', response_model=List[PlaylistMeta])
async def all_playlists() -> List[PlaylistMeta]:
    all_ids = [playlist.to_dict().get('id') for playlist in await Playlist.query.where(Playlist.public).gino.all()]
    all_pl = [await playlist_dict(i) for i in all_ids]
    print(all_pl)
    return all_pl


@playlists.get('/playlist/get',  response_model=PlaylistMeta)
async def get_playlist(id: int) -> PlaylistMeta or JSONResponse:
    if playlist := await playlist_dict(id):
        if playlist.get('public'):
            return playlist
        else:
            return JSONResponse(status_code=403, content={'result': 'this playlist is private', 'status': 403})
    else:
        return JSONResponse(status_code=404, content={'result': 'no playlist', 'status': 404})


@playlists.post('/playlist/update/')
async def add_to_playlist(playlist_x_track: PlaylistXTrackMeta) -> JSONResponse:
    response = await playlist_update(playlist_x_track.playlist_id, playlist_x_track.track_id)
    return JSONResponse(status_code=response['status'], content={'result': response['result']})


@playlists.delete('/playlist/update/')
async def delete_from_playlist(playlist_x_track: PlaylistXTrackMeta) -> JSONResponse:
    response = await playlist_delete_from(playlist_x_track.playlist_id, playlist_x_track.track_id)
    return JSONResponse(status_code=response['status'], content={'result': response['result']})
