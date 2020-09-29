from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session

database_url = 'postgres://postgres:postgres@localhost:8002'

engine = create_engine(database_url)
session_factory = sessionmaker(bind=engine, autoflush=False)
session = scoped_session(session_factory) #type: Session

Base = declarative_base()


class Track(Base):
    __tablename__ = 'track'
    Column('track_id', Integer, primary_key=True),
    Column('track_name', String),
    Column('track_year', Integer)


# artist = Table(
#     'artist',
#     Column('artist_id', Integer),
#     Column('album_name', String),
#     Column('album_year', Integer),
#     Column('Track', String)
# )
#
# album = Table(
#     'album',
#     Column('album_id', Integer),
#     Column('album_name', String),
#     Column('album_year', Integer))
