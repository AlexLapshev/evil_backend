from asyncpg.pool import Pool

from api.database.db_track import TrackCRUD
from api.database.db_transactions import DatabaseTransactions


class ReleaseCRUD:
    """Операции над релизами"""
    def __init__(self, pool: Pool):
        self.pool = pool

    async def get_one_release(self, release_id: int) -> dict:
        if release := await DatabaseTransactions(self.pool) \
                .select('''SELECT * FROM releases WHERE release_id={}''', release_id):
            release['tracks'] = await TrackCRUD(self.pool).get_tracks_by_release_id(release_id)
            return release
        else:
            raise ValueError("release {} not found".format(release_id))

    async def get_one_release_with_track_ids(self, release_id):
        release = await self.get_one_release(release_id)
        track_ids = [track['track_id'] for track in release.get('tracks')]
        release['tracks'] = track_ids
        return release

    async def get_all_releases(self, q: int = 8) -> list:
        all_rel = await DatabaseTransactions(self.pool) \
            .select_multiple('''SELECT * FROM releases LIMIT {} '''.format(q))
        for index, release in enumerate(all_rel):
            if tracks := await TrackCRUD(self.pool).get_tracks_by_release_id(release['release_id']):
                all_rel[index]['tracks'] = tracks
            else:
                all_rel[index]['tracks'] = []
        return all_rel
