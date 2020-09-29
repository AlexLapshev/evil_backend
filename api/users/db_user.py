import logging

from asyncpg.pool import Pool
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from api.auth.main import get_current_active_user
from api.database.database import get_mongo_client
from api.database.db_transactions import DatabaseTransactions

logger = logging.getLogger(__name__)


class UserCRUD:
    """Получение пользовательских данных из postgres"""

    def __init__(self, pool: Pool):
        self.pool = pool

    async def get_user(self, user_id):
        if user_info := await DatabaseTransactions(self.pool).select('''SELECT * FROM users WHERE user_id = {}''', user_id):
            return user_info
        else:
            raise ValueError('no user found')

    async def get_user_by_email(self, decoded_email: str) -> dict:
        if user := await DatabaseTransactions(self.pool)\
                .select('''SELECT * FROM users WHERE email = {}''', decoded_email):
            return user
        raise ValueError('invalid token')

    async def activate_user(self, user_id):
        await DatabaseTransactions(self.pool).execute('''UPDATE users SET active = True WHERE user_id = {}''', user_id)


class UserCrudMongo:
    """Получение пользовательских данных из монго"""

    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.mongo_client = mongo_client

    async def get_user_info(self, user_id: int) -> dict:
        return await self.mongo_client.play_backend_mongo.user_likes.find_one({'_id': user_id})

    async def update_user_info(self, user_id: int, user_info: dict) -> None:
        await self.mongo_client.play_backend_mongo.user_likes.replace_one({'_id': user_id}, user_info)


class UserInfoUpdate:
    """Обновление пользовательских данных в монго"""
    @staticmethod
    def add_track_to_user_playlist(user_info: dict, playlist_id: int, track_id: int) -> dict:
        for playlist in user_info['playlists']:
            if playlist['playlist_id'] == playlist_id:
                playlist['tracks'].append(track_id)
        return user_info

    @staticmethod
    def delete_track_from_user_playlist(user_info: dict, playlist_id: int) -> dict:
        for index_pl, playlist in enumerate(user_info['playlists']):
            if playlist['playlist_id'] == playlist_id:
                for index_tr, track_id in enumerate(playlist['tracks']):
                    if track_id == track_id:
                        del user_info['playlists'][index_pl]['tracks'][index_tr]
        return user_info

    @staticmethod
    def delete_playlist_from_user_playlists(user_info: dict, playlist_id: int) -> dict:
        for index, playlist in enumerate(user_info['playlists']):
            if playlist['playlist_id'] == playlist_id:
                del user_info['playlists'][index]
        return user_info

    @staticmethod
    def unlike_track(user_info: dict, track_id: int) -> dict:
        user_tracks = user_info.get('tracks')
        for index, track in enumerate(user_tracks):
            if track.get('track_id') == track_id:
                logger.debug('found track to unlike')
                del user_info['tracks'][index]
        return user_info

    @staticmethod
    def unlike_release(user_info: dict, release_id: int) -> dict:
        user_releases = user_info.get('releases')
        for index, release in enumerate(user_releases):
            if release.get('release_id') == release_id:
                logger.debug('found release to unlike')
                del user_info['releases'][index]
        return user_info


# зависимсость - информацаия о пользователе:
async def _user_info_dependency(current_user=Depends(get_current_active_user),
                                mongo_client: AsyncIOMotorClient = Depends(get_mongo_client)) -> dict:
    user_id = current_user.get('user_id')
    user_info = await UserCrudMongo(mongo_client).get_user_info(user_id)
    return user_info
