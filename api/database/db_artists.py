from api.database.db_release import release_dict
from api.database.models import Track, Artist, Release
from api.database.database import db


async def get_artist(artist_id: int) -> Artist:
    artist = await Artist.query.where(Artist.id == artist_id).gino.first()
    return artist


async def artist_releases_dict(artist_id: int) -> list:
    artist_releases = await db.select([Release]).\
        where(Release.artist_id == artist_id).gino.load(Release.id).all()
    artist = await get_artist(artist_id)
    artist = artist.to_dict()
    artist_releases = [await release_dict(artist_id, True) for artist_id in artist_releases]
    artist['releases'] = artist_releases
    return artist


async def artist_tracks_dict(artist_id: int) -> dict:
    artist_tracks = await db.select([Track]).where(Artist.id == artist_id).gino.load(
     (
            Artist.id,
            Track.artists_id,
            Track.track_name,
            [track.to_dict() for track in await Track.query.where(Track.artists_id == artist_id).gino.all()]
    )
    ).first()
    artist_tracks= dict(zip(['id', 'artist', 'track_name'], artist_tracks))
    return artist_tracks
