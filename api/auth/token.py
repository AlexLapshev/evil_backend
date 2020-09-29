import logging
from datetime import timedelta

from asyncpg.pool import Pool
from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from jose import ExpiredSignatureError
from starlette.requests import Request
from starlette.responses import JSONResponse

from api.auth.api_types import TokenMeta
from api.auth.main import authenticate_user
from api.auth.email_confirmation import send_email_confirm
from api.auth.jwt_work import create_access_token, decode_token
from api.auth.secret import SECRET_KEY_REFRESH
from api.database.database import get_connection

token = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24*30

logger = logging.getLogger(__name__)


@token.post("/token", response_model=TokenMeta)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 pool: Pool = Depends(get_connection)) -> JSONResponse:
    if user := await authenticate_user(form_data.username, form_data.password, pool):
        logging.debug('authenticating user {}'.format(user.get('username')))
        if user.get('active'):
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.get('username')}, expires_delta=access_token_expires
            )
            ref_token = create_access_token(
                data={"sub": user.get('username')}, expires_delta=access_token_expires, secret_key=SECRET_KEY_REFRESH
            )
            return JSONResponse(content={"access_token": access_token,
                                         "refresh_token": ref_token,
                                         "token_type": "bearer", }, status_code=200)
        else:
            send_email_confirm(user.email)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="message was sent to {}".format(user.email),
                headers={"WWW-Authenticate": "Bearer"},
            )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


@token.post("/refresh-token")
async def refresh_token(request: Request):
    try:
        access_token_expires = timedelta(minutes=60*24*60)
        logger.debug('creating refresh token')
        decoded = decode_token(request.headers['refresh_token'], SECRET_KEY_REFRESH)
        logger.debug('decoded: ', decoded)
        access_token = create_access_token(data={"sub": decoded['sub']}, expires_delta=access_token_expires)
        logger.debug('access_token: ', access_token)
        ref_token = create_access_token(data={"sub": decoded['sub']}, expires_delta=access_token_expires,
                                        secret_key=SECRET_KEY_REFRESH)
        return {"access_token": access_token, "token_type": "bearer", "refresh_token": ref_token}
    except ValueError as e:
        return JSONResponse(status_code=401, content='invalid credentials')
    except ExpiredSignatureError as e:
        return JSONResponse(status_code=401, content='refresh-token has expired',
                            headers={"access-control-allow-origin": "*"})
