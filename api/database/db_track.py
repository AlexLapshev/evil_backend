from gino.declarative import ModelType
from api.database.models import db, Track, Release, Artist, PlaylistXTrack


async def select_track(track_id: int) -> ModelType:
    track = await db.select([Track.id, Track.name, Track.lyrics, Release.id, Release.name, Release.date, Artist.id,
                             Artist.name]).select_from(Track.join(Release).join(Artist)).\
        where(Track.id == track_id).gino.first()
    return track


async def create_list(release_id: int) -> list:
    all_tracks = [await select_track(track.id) for track in
                  await Track.query.where(Track.release_id == release_id).gino.all()]
    return [await track_do_dict(track) for track in all_tracks]


async def track_do_dict(track: ModelType, prefix: bool = True) -> dict:
    values = ['track_id', 'track_name', 'track_lyrics', 'release_id',
              'release_name', 'release_date', 'artist_id', 'artist_name']
    if not prefix:
        values = [value.replace('track_', '') for value in values]
    return dict(zip(values, track))


async def all_playlist_tracks(playlist_id):
    all_tracks = [await select_track(track.id) for track in await Track.query.where(Track.id == PlaylistXTrack.track_id).
        where(PlaylistXTrack.playlist_id == playlist_id).gino.all()]
    return [await track_do_dict(track) for track in all_tracks]
