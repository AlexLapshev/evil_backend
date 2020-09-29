import asyncpg
import asyncio
import json
import motor.motor_asyncio
import pytest

from fastapi.testclient import TestClient
from api.auth.secret import DB_USER, DB_PASSWORD


async def insert_in_mongo(mongo_client, dump):
    dumped = json.load(dump)
    await mongo_client.play_backend_mongo.user_likes.insert_many([document for document in dumped])


@pytest.fixture(scope="session")
def client():
    from api.main import app
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def access_token():
    from api.main import app
    with TestClient(app) as client:
        r = client.post(
            '/api/v1/token',
            data={'username': 'johndoe', 'password': 'secret'}
        )
        token = r.json().get('access_token')
        yield token


@pytest.fixture(scope="session", autouse=True)
def main():
    sql_file = open('api/tests/dump.sql')
    mongo_file = open('api/tests/dumpmongo.json')
    connection = asyncio.get_event_loop().run_until_complete(asyncpg.connect(host='localhost', database='play_backend_db', user=DB_USER, password=DB_PASSWORD))
    mongo_client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{DB_USER}:{DB_PASSWORD}@0.0.0.0:27017/play_backend_mongo")
    asyncio.get_event_loop().run_until_complete(connection.execute(sql_file.read()))
    asyncio.get_event_loop().run_until_complete(insert_in_mongo(mongo_client, mongo_file))
    yield
    asyncio.get_event_loop().run_until_complete(connection.execute('''DROP SCHEMA public CASCADE; CREATE SCHEMA public;'''))
    asyncio.get_event_loop().run_until_complete(mongo_client.play_backend_mongo.user_likes.delete_many({"_id": 1}))
