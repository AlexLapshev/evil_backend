from api.database.models import Release, Artist
from api.database.database import db
from api.database.db_track import create_list


async def release_dict(release_id: int, prefix: bool = False) -> dict or None:
    if release := await db.select([Release, Artist]).where(Release.id == release_id).\
            where(Artist.id == Release.artist_id).gino.\
            load((Artist.id, Artist.name, Release.id, Release.name,
                  Release.date, await create_list(release_id))).first():
        return await track_do_dict(release, prefix)


async def track_do_dict(release, prefix: bool = True) -> dict:
    values = ['artist_id', 'artist_name', 'release_id', 'release_name', 'release_date', 'tracks']
    if not prefix:
        values = [value.replace('release_', '') for value in values]
    return dict(zip(values, release))
