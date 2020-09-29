import logging

from passlib.context import CryptContext
from jose import JWTError, ExpiredSignatureError

from asyncpg.pool import Pool

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from api.auth.jwt_work import decode_token
from api.auth.api_types import TokenDataMeta
from api.database.db_transactions import DatabaseTransactions
from api.database.database import get_connection

pwd_context = CryptContext(schemes=["sha512_crypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

logger = logging.getLogger(__name__)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str, pool: Pool) -> dict or bool:
    user = await DatabaseTransactions(pool).select('''SELECT * FROM users WHERE username = '{}' ''', username)
    if not user:
        return False
    if not verify_password(password, user.get('hash_password')):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), pool: Pool = Depends(get_connection)) -> dict:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenDataMeta(username=username)
    except ExpiredSignatureError as exc:
        raise HTTPException(status_code=401, detail="Expired token", headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise credentials_exception
    user = await DatabaseTransactions(pool)\
        .select('''SELECT * FROM users WHERE username = '{}' ''', token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user.get('disabled'):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
