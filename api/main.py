import asyncpg
import logging.config
import motor.motor_asyncio
import uvicorn


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from starlette.middleware.authentication import AuthenticationMiddleware
from api.auth.secret import DB_USER, DB_PASSWORD
from api.artists import artists
from api.auth.token import token
from api.middleware.authentication_middleware import on_auth_error
from api.middleware.authentication_middleware import BasicAuthBackend
from api.playlists import playlists
from api.realeses import releases
from api.tracks import tracks
from api.users.users import users

logging.config.fileConfig(Path.joinpath(Path(__file__).parent, 'logging.conf'), disable_existing_loggers=False)


def create_app():
    app = FastAPI(debug=True)
    origins = [
        "http://0.0.0.0:8080",
        "http://localhost:8080",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(AuthenticationMiddleware,
                       backend=BasicAuthBackend(),
                       on_error=on_auth_error
                       )
    app.include_router(tracks, prefix='/api/v1', tags=['tracks'])
    app.include_router(releases, prefix='/api/v1', tags=['releases'])
    app.include_router(playlists, prefix='/api/v1', tags=['playlists'])
    app.include_router(artists, prefix='/api/v1', tags=['artists'])
    app.include_router(token, prefix='/api/v1', tags=['token'])
    app.include_router(users, prefix='/api/v1/users', tags=['users'])
    app.router.add_event_handler("startup", create_startup_hook(app))
    return app


def create_startup_hook(app: FastAPI):
    async def startup_hook() -> None:
        app.state.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{DB_USER}:{DB_PASSWORD}@0.0.0.0:27017/play_backend_mongo")
        app.state.pool = await asyncpg.create_pool(dsn=f"postgres://{DB_USER}:{DB_PASSWORD}@0.0.0.0:5432/play_backend_db")
    return startup_hook


app = create_app()


if __name__ == "__main__":
    uvicorn.run('api.main:app', host="0.0.0.0", port=1984, reload=True, workers=4)
