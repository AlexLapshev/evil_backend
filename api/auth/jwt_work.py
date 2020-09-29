import logging

from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from typing import Optional

from api.auth.secret import SECRET_KEY, ALGORITHM

logger = logging.getLogger(__name__)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None, secret_key=SECRET_KEY) -> str:
    logging.debug('creating access token')
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token, secret_key=SECRET_KEY):
    logging.debug('decoding token')
    try:
        decoded_jwt = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return decoded_jwt
    except ExpiredSignatureError as e:
        logger.debug('expired token')
        raise ExpiredSignatureError('Token has expired')
    except JWTError as e:
        logger.debug('invalid token')
        raise ValueError('Invalid basic auth credentials')
