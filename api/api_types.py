from pydantic import BaseModel, conint, StrictStr
from typing import List
from datetime import date

from api.auth.api_types import UserMeta


class TrackBaseMeta(BaseModel):
    id: conint(ge=1, le=1000000000000)
    name: StrictStr
    lyrics: StrictStr


class TrackNestedMeta(BaseModel):
    track_id: conint(ge=1, le=1000000000000)
    track_name: StrictStr
    track_lyrics: StrictStr


class TrackWithArtistMeta(BaseModel):
    artist_id: conint(ge=1, le=10000000000)
    artist_name: str


class TrackWithReleaseMeta(BaseModel):
    release_id: conint(ge=1, le=10000000000)
    release_name: str
    release_date: date


class TrackPlaylistMeta(TrackWithArtistMeta, TrackWithReleaseMeta, TrackNestedMeta):
    pass


class TrackFullMeta(TrackWithArtistMeta, TrackWithReleaseMeta, TrackBaseMeta):
    pass


class TrackReleaseMeta(TrackWithReleaseMeta):
    tracks: List[TrackNestedMeta]
    pass


class ArtistMeta(BaseModel):
    id: conint(ge=1, le=10000000000)
    name: StrictStr


class ReleaseBaseMeta(BaseModel):
    id: conint(ge=1, le=10000000000)
    name: StrictStr
    date: date
    tracks: List[TrackNestedMeta]


class ReleaseWithArtistMeta(ReleaseBaseMeta):
    artist_id: conint(ge=1, le=10000000000)
    artist_name: StrictStr


class PlaylistMeta(BaseModel):
    id: conint(ge=1, le=10000000)
    name: StrictStr
    public: bool
    tracks: List[TrackPlaylistMeta]


class ResultMeta(BaseModel):
    result: StrictStr
    status: conint(ge=200, le=600)


class PlaylistXTrackMeta(BaseModel):
    playlist_id: int
    track_id: int


class ArtistxReleasesMeta(ArtistMeta):
    releases: List[TrackReleaseMeta]



class UserPlaylistMeta(UserMeta):
    playlists: List[PlaylistMeta]
