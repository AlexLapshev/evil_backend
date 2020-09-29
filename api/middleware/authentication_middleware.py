from jose import ExpiredSignatureError
from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, SimpleUser,
    AuthCredentials
)

import binascii

from starlette.requests import Request
from starlette.responses import JSONResponse

from api.auth.jwt_work import decode_token


def on_auth_error(request: Request, exc: Exception):
    return JSONResponse({"error": str(exc)}, status_code=401, headers={"access-control-allow-origin": "*"})


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return

        auth = request.headers["Authorization"]

        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'bearer':

                return
            decoded = decode_token(credentials)

        except ExpiredSignatureError as exc:
            raise AuthenticationError('Token has expired')

        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError('Invalid basic auth credentials')

        username = decoded.get('sub')
        return AuthCredentials(["authenticated"]), SimpleUser(username)
