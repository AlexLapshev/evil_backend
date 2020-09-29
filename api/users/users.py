import datetime
import logging

from asyncpg import UniqueViolationError
from asyncpg.pool import Pool
from fastapi import APIRouter, Depends, UploadFile, File, Form
from motor.motor_asyncio import AsyncIOMotorClient
from pathlib import Path

from starlette.requests import Request
from starlette.responses import JSONResponse
from jose import JWTError, ExpiredSignatureError

from api.auth.main import get_current_active_user
from api.auth.jwt_work import decode_token
from api.database.database import get_connection, get_mongo_client
from api.database.db_playlist import PlaylistCRUD
from api.database.db_releases import ReleaseCRUD
from api.database.db_track import TrackCRUD
from api.users.api_types import UserInfo
from api.users.db_user import UserCrudMongo, UserCRUD, _user_info_dependency, UserInfoUpdate
from api.database.db_artist import ArtistCRUD

users = APIRouter()

logger = logging.getLogger(__name__)


@users.get("/me", response_model=UserInfo)
async def user(current_user=Depends(get_current_active_user),
               mongo_client: AsyncIOMotorClient = Depends(get_mongo_client), pool: Pool = Depends(get_connection)):
    user_id = current_user.get('user_id')
    try:
        user_info = await UserCRUD(pool).get_user(user_id)
    except ValueError as e:
        return JSONResponse(content={'error': str(e)}, status_code=404)
    logging.debug(f'user_id: {user_id}')
    user_like_info = await mongo_client.play_backend_mongo.user_likes.find_one({"_id": user_id})
    user_like_info['username'] = user_info.get('username')
    return user_like_info


@users.get("/confirm/{hash_email}")
async def confirm_user_email(hash_email: str, pool: Pool = Depends(get_connection)) -> JSONResponse:
    try:
        decoded = decode_token(hash_email)
        decoded_email = decoded.get('email')
    except ExpiredSignatureError:
        return JSONResponse(status_code=401, content={"status": "expired token"})
    except JWTError:
        return JSONResponse(status_code=401, content={"status": "invalid token"})
    try:
        user = await UserCRUD(pool).get_user_by_email(decoded_email)
    except ValueError as e:
        return JSONResponse(content={'error': str(e)}, status_code=403)
    logger.debug(f'user is {user}')
    if user.get('active'):
        return JSONResponse(status_code=409, content={"status": "user is already activated"})
    await UserCRUD(pool).activate_user(user['user_id'])
    return JSONResponse(status_code=200, content={"status": "{} successfully activated".format(decoded_email)})


@users.post("/track/{track_id}/like")
async def user_like_track(track_id: int,
                          current_user=Depends(get_current_active_user),
                          mongo_client=Depends(get_mongo_client),
                          pool: Pool = Depends(get_connection),
                          user_info: dict = Depends(_user_info_dependency)):
    track_ids = [track['track_id'] for track in user_info.get('tracks')]
    if track_id in track_ids:
        return JSONResponse(status_code=409, content='track is already liked')
    else:
        logger.debug('getting track from db, track_id: {}'.format(track_id))
        track = await TrackCRUD(pool).get_one_track(track_id)
        user_info['tracks'].append(track)
        await UserCrudMongo(mongo_client).update_user_info(user_info['_id'], user_info)
        return JSONResponse(status_code=201, content={'result': 'success'})


@users.delete("/track/{track_id}/like")
async def user_unlike_track(track_id: int,
                            mongo_client=Depends(get_mongo_client),
                            user_info: dict = Depends(_user_info_dependency)):
    track_ids = [track['track_id'] for track in user_info.get('tracks')]
    if track_id not in track_ids:
        return JSONResponse(status_code=409, content='track is not liked')
    else:
        logger.debug('unliking track: {}'.format(track_id))
        user_info = UserInfoUpdate.unlike_track(user_info, track_id)
        await UserCrudMongo(mongo_client).update_user_info(user_info['_id'], user_info)
        return JSONResponse(status_code=201, content='track unliked')


@users.post("/artist/{artist_id}/subscribe")
async def user_subscribe_artist(artist_id: int,
                                mongo_client=Depends(get_mongo_client), pool: Pool = Depends(get_connection),
                                user_info: dict = Depends(_user_info_dependency)):
    artist_ids = [artist['artist_id'] for artist in user_info.get('artists')]
    if artist_id in artist_ids:
        return JSONResponse(status_code=409, content='user is already subscribed to artist')
    else:
        logger.debug('getting artist from db, artist_id: {}'.format(artist_id))
        try:
            artist = await ArtistCRUD(pool).get_artist_with_release_ids(artist_id)
            user_info['artists'].append(artist)
            await UserCrudMongo(mongo_client).update_user_info(user_info['_id'], user_info)
            return JSONResponse(status_code=201, content='user has subscribed to artist')
        except ValueError as e:
            return JSONResponse(status_code=404, content=str(e))


@users.delete("/artist/{artist_id}/subscribe")
async def user_unsubscribe_artist(artist_id: int,
                                  mongo_client=Depends(get_mongo_client),
                                  user_info: dict = Depends(_user_info_dependency)):
    artist_ids = [artist['artist_id'] for artist in user_info.get('artists')]
    if artist_id in artist_ids:
        logger.debug('getting artist from db, artist_id: {}'.format(artist_id))
        for index, ar_id in enumerate(artist_ids):
            if ar_id == artist_id:
                logger.debug('found artist to unsubscribe')
                del user_info['artists'][index]
                await UserCrudMongo(mongo_client).update_user_info(user_info['_id'], user_info)
                return JSONResponse(status_code=201, content='user has unsubscribed from artist')
    else:
        return JSONResponse(status_code=409, content="user is not subscribe to artist")


@users.post('/playlist/{playlist_id}')
async def add_to_playlist(playlist_id: int, track_id: int, pool: Pool = Depends(get_connection),
                          user_info=Depends(_user_info_dependency),
                          mongo_client: AsyncIOMotorClient = Depends(get_mongo_client)) -> JSONResponse:
    playlist_ids = [playlist['playlist_id'] for playlist in user_info['playlists']]
    if playlist_id in playlist_ids:
        logger.debug('found playlist')
        try:
            await PlaylistCRUD(pool).add_track_to_playlist(playlist_id, track_id)
        except ValueError as e:
            return JSONResponse(content={'error': str(e)})
        user_info = UserInfoUpdate.add_track_to_user_playlist(user_info, playlist_id, track_id)
        await UserCrudMongo(mongo_client).update_user_info(user_info['_id'], user_info)
        return JSONResponse(content={'result': 'track added'}, status_code=201)
    else:
        logger.debug('foreign playlist')
        return JSONResponse(status_code=403, content={'error': 'foreign playlist'})


@users.delete('/playlist/{playlist_id}')
async def delete_from_playlist(playlist_id: int,
                               track_id: int,
                               pool: Pool = Depends(get_connection),
                               user_info=Depends(_user_info_dependency),
                               motor_client: AsyncIOMotorClient = Depends(get_mongo_client)) -> JSONResponse:
    user_id = user_info['_id']
    playlist_ids = [playlist['playlist_id'] for playlist in user_info['playlists']]
    if playlist_id in playlist_ids:
        logger.debug('found playlist in user playlists')
        try:
            await PlaylistCRUD(pool).delete_track_from_playlist(playlist_id, track_id)
        except ValueError as e:
            return JSONResponse(content={'error': str(e)})
        user_info = UserInfoUpdate.delete_track_from_user_playlist(user_info, playlist_id)
        await UserCrudMongo(motor_client).update_user_info(user_id, user_info)
        return JSONResponse(status_code=200, content={'result': 'track deleted'})
    else:
        logger.debug('playlist not found in user playlists')
        return JSONResponse(status_code=403, content={'error': 'foreign playlist'})


@users.post('/playlists')
async def create_user_playlist(request: Request,
                               playlist_name: str = Form(...),
                               playlist_public: bool = Form(False),
                               pool: Pool = Depends(get_connection),
                               playlist_cover: UploadFile = File(None),
                               user_info: dict = Depends(_user_info_dependency),
                               mongo_client: AsyncIOMotorClient = Depends(get_mongo_client)):
    user_id = int(user_info['_id'])
    if playlist_cover:
        extension = playlist_cover.filename.split('.')[-1]
        if extension not in ['jpg', 'jpeg', 'png']:
            return JSONResponse(content={'error': 'this type of image is not supported'}, status_code=409)
        if int(request.headers['content-length']) / 1048576 > 1:
            return JSONResponse(content={'error': 'image size is too big'}, status_code=409)
        image_name = f'user_{user_id}_playlist_{playlist_name}.{extension}'
    else:
        image_name = 'playlist.png'
    logger.debug('creating new playlist')
    try:
        playlist = await PlaylistCRUD(pool).create_playlist(playlist_name, playlist_public, image_name, user_id)
    except UniqueViolationError as e:
        return JSONResponse(content={'error': 'there is a playlist with this name'}, status_code=409)
    user_info['playlists'].append(playlist)
    await UserCrudMongo(mongo_client).update_user_info(user_info['_id'], user_info)
    path = Path(__file__).parent.parent.parent.parent
    path = path / 'evil_frontend/src/assets/covers/playlists/'
    if playlist_cover:
        image = await playlist_cover.read()
        with open(path / image_name, "wb") as img:
            img.write(image)
    return JSONResponse(status_code=201, content={'result': 'playlist created'})


@users.delete('/playlists')
async def remove_user_playlist(playlist_id: int,
                               pool: Pool = Depends(get_connection),
                               user_info: dict = Depends(_user_info_dependency),
                               mongo_client: AsyncIOMotorClient = Depends(get_mongo_client)):
    logger.debug('deleting playlist')
    await PlaylistCRUD(pool).delete_playlist(playlist_id, user_info['_id'])
    user_info = UserInfoUpdate.delete_playlist_from_user_playlists(user_info, playlist_id)
    await UserCrudMongo(mongo_client).update_user_info(user_info['_id'], user_info)
    return JSONResponse(status_code=200, content={'result': 'playlist deleted'})


@users.post("/release/{release_id}/like")
async def user_like_track(release_id: int,
                          mongo_client=Depends(get_mongo_client),
                          pool: Pool = Depends(get_connection),
                          user_info: dict = Depends(_user_info_dependency)):
    release_ids = [release['release_id'] for release in user_info.get('releases')]
    if release_id in release_ids:
        return JSONResponse(status_code=409, content={'error': 'release is already liked'})
    else:
        logger.debug(f'getting release from db, release_id: {release_id}')
        release = await ReleaseCRUD(pool).get_one_release_with_track_ids(release_id)
        release['release_year'] = datetime.datetime.combine(release['release_year'],
                                                            datetime.datetime.strptime('00:00', '%H:%M').time())
        user_info['releases'].append(release)
        await UserCrudMongo(mongo_client).update_user_info(user_info['_id'], user_info)
        return JSONResponse(status_code=201, content={'result': 'release liked'})


@users.delete("/release/{release_id}/like")
async def user_like_track(release_id: int,
                          mongo_client=Depends(get_mongo_client),
                          user_info: dict = Depends(_user_info_dependency)):
    release_ids = [release['release_id'] for release in user_info.get('releases')]
    if release_id in release_ids:
        user_info = UserInfoUpdate.unlike_release(user_info, release_id)
        await UserCrudMongo(mongo_client).update_user_info(user_info['_id'], user_info)
        return JSONResponse(status_code=200, content='release unliked')
    else:
        return JSONResponse(status_code=409, content='release is not liked')
