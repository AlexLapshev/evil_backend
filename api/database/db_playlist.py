from api.database.models import Playlist, PlaylistXTrack, Track, db, Release, Artist
from api.database.db_track import select_track, all_playlist_tracks


# Вспомогательная проверяет наличие плейлиста
async def check_playlist(playlist_id: int) -> bool:
    return await Playlist.query.where(Playlist.id == playlist_id).gino.first()


# Вспомогательная проверяет наличие трека
async def check_track(track_id: int) -> bool:
    return await Track.query.where(Track.id == track_id).gino.first()


async def playlist_dict(playlist_id: int) -> dict or None:
    if await check_playlist(playlist_id):
        playlist = await db.select([Playlist, Track, PlaylistXTrack])\
            .where(Playlist.id == playlist_id).gino.load(
            (
                Playlist.id,
                Playlist.name,
                Playlist.public,
                await all_playlist_tracks(playlist_id)
            )
        ).first()
        playlist = dict(zip(('id', 'name', 'public', 'tracks'), playlist))
    else:
        return
    return playlist


async def playlist_update(playlist_id: id, track_id: int) -> dict:
    if await check_playlist(playlist_id) and await check_track(track_id):
        if await PlaylistXTrack.query.where(PlaylistXTrack.playlist_id == playlist_id)\
                .where(PlaylistXTrack.track_id == track_id).gino.first():
            return {'result': 'track is in playlist', 'status': 409}
        else:
            play_x_tr = PlaylistXTrack(playlist_id=playlist_id, track_id=track_id)
            await play_x_tr.create()
            return {'result': 'track added', 'status': 201}
    else:
        return {'result': 'playlist or track not found', 'status': 404}


async def playlist_delete_from(playlist_id: id, track_id: int) -> dict:
    if await PlaylistXTrack.query.where(PlaylistXTrack.playlist_id == playlist_id) \
            .where(PlaylistXTrack.track_id == track_id).gino.first():
        await PlaylistXTrack.delete. \
            where(PlaylistXTrack.playlist_id == playlist_id) \
            .where(PlaylistXTrack.track_id == track_id).gino.status()
        return {'result': 'track deleted', 'status': 200}
    else:
        return {'result': 'no track in playlist or no playlist', 'status': 404}

