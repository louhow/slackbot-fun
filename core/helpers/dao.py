from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import IntegrityError
from slackbot_settings import SPOTIFY_DEFAULT_PLAYLIST_ID
from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy.util import KeyedTuple

Base = declarative_base()


class Dao(object):
  def __init__(self):
    engine = create_engine('mysql+pymysql://user:pass@127.0.0.1:14306/slackbot-db',
                           pool_recycle=280,
                           pool_pre_ping=True)
    session_factory = sessionmaker(bind=engine)
    self.Session = scoped_session(session_factory)


  def query_all(self, file_name):
    f = open('backup.txt', 'wb')
    session = self.Session()
    try:
      q = session.query(SpotifyTrack)
      f.write(dumps(q.all()))
      f.close()
    finally:
      session.close()


  def load(self, file_name):
    with open(file_name, 'rb') as file_handler:
      session = self.Session()
      try:
        for row in loads(file_handler.read()):
          if isinstance(row, KeyedTuple):
            row = SpotifyTrack(**row._asdict())
          session.merge(row)

        session.commit()
      finally:
        session.close()


  def get_spotify_track(self, external_track_id):
    """
    :param external_track_id:
    :return: SpotifyTrack
    """
    session = self.Session()
    try:
      result = session.query(SpotifyTrack) \
        .filter_by(external_track_id=external_track_id, external_playlist_id=SPOTIFY_DEFAULT_PLAYLIST_ID) \
        .first()
    finally:
      session.close()

    return result


  def insert_spotify_tracks(self, track_ids):
    for track_id in track_ids:
      if self.get_spotify_track(track_id) is None:
        self.insert_spotify_track(track_id)

  def insert_spotify_track(self, track_id, user_id=None):
    success = False
    s = self.Session()
    try:
      s.add(SpotifyTrack(
        external_track_id=track_id,
        external_playlist_id=SPOTIFY_DEFAULT_PLAYLIST_ID,
        create_slack_user_id=user_id
      ))
      s.commit()
      success = True
    except IntegrityError:
      print(f'Unable to add duplicate track {track_id}')
      success = True
    except Exception as e:
      print(e)
    finally:
      s.close()

    return success



class SpotifyTrack(Base):
  __tablename__ = 'spotify_track'
  spotify_track_id = Column(Integer, primary_key=True)
  external_playlist_id = Column(String(20))
  external_track_id = Column(String(20))
  create_slack_user_id = Column(String(20))
  create_time = Column(TIMESTAMP)

  def __str__(self):
    return '%(spotify_track_id)s' % locals()
