from pydantic import BaseModel
from typing import Optional


class TokenMeta(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenDataMeta(BaseModel):
    username: Optional[str] = None


class UserMeta(BaseModel):
    id: int
    username: str
    email: str
    disabled: bool


class UserInDBMeta(UserMeta):
    hash_password: str
