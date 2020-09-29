import logging

from asyncpg.pool import Pool

from api.database.db_transactions import DatabaseTransactions

logger = logging.getLogger(__name__)


class ArtistCRUD:
    def __init__(self, pool: Pool):
        self.pool = pool

    async def get_all_artists(self, q: int = 8) -> list:
        all_artists = await DatabaseTransactions(self.pool) \
            .select_multiple('''SELECT * FROM artists LIMIT {} '''.format(q))
        for index, artist in enumerate(all_artists):
            all_artists[index]['releases'] = await DatabaseTransactions(self.pool) \
                .select_multiple('''SELECT * FROM releases WHERE artist_id = {}''', artist.get('artist_id'))
        return all_artists

    async def get_artist_with_releases(self, artist_id):
        if artist := await DatabaseTransactions(self.pool) \
                .select('''SELECT * FROM artists WHERE artist_id = {};''', artist_id):
            artist['releases'] = await DatabaseTransactions(self.pool) \
                .select_multiple('''SELECT * FROM releases WHERE artist_id = {}''', artist.get('artist_id'))
            return artist
        raise ValueError('no artist found')

    async def get_artist_with_release_ids(self, artist_id):
        if artist := await self.get_artist_with_releases(artist_id):
            artist_releases = [release for release in artist['releases']]
            artist_release_ids = [release['release_id'] for release in artist_releases]
            logger.debug('release ids: ', artist_release_ids)
            artist['releases'] = artist_release_ids
            return artist
        raise ValueError('no artist found')
