from api.database.database import db
from api.auth.models import User


class Release(db.Model):
    __tablename__ = 'releases'
    id = db.Column(db.Integer(), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    name = db.Column(db.VARCHAR(length=255))
    date = db.Column(db.Date())


class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.VARCHAR(length=255))


class Track(db.Model):
    __tablename__ = 'tracks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(length=255))
    lyrics = db.Column(db.String)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    release_id = db.Column(db.Integer, db.ForeignKey('releases.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._playlists = set()

    @property
    def playlists(self):
        return self._playlists


class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(length=255))
    public = db.Column(db.BOOLEAN(), default=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tracks = set()

    @property
    def tracks(self):
        return self._tracks

    def add_track(self, track):
        self._tracks.add(track)
        track._parents.add(self)


class PlaylistXTrack(db.Model):
    __tablename__ = 'playlists_x_tracks'

    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'))
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'))


class UserXPlaylist(db.Model):
    __tablename__ = 'user_x_playlist'

    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
