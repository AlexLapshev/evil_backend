from pydantic import BaseModel, StrictStr
from typing import List, Optional
from datetime import date


from api.api_types import TrackMeta


class UserArtistMeta(BaseModel):
    artist_id: int
    artist_name: StrictStr
    artist_cover: StrictStr
    releases: List[int]


class UserReleaseMeta(BaseModel):
    release_id: int
    artist_id: int
    release_name: StrictStr
    release_cover: Optional[StrictStr]
    release_year: date
    tracks: List[int]


class UserPlaylistMeta(BaseModel):
    playlist_id: int
    playlist_name: StrictStr
    public: bool
    tracks: List[int]
    playlist_cover: Optional[StrictStr]


class UserInfo(BaseModel):
    username: str
    artists: list
    releases: list
    tracks: list
    playlists: list
