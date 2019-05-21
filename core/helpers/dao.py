from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from slackbot_settings import SPOTIFY_DEFAULT_PLAYLIST_ID

Base = declarative_base()

class Dao(object):
  def __init__(self):
    engine = create_engine('mysql+pymysql://root:pass@localhost:14306/mariadb')
    self.Session = sessionmaker()
    self.Session.configure(bind=engine)

  def get_spotify_track(self, external_track_id):
    """
    :param external_track_id:
    :return: SpotifyTrack
    """
    session = self.Session()
    result = session.query(SpotifyTrack) \
      .filter_by(external_track_id=external_track_id, external_playlist_id=SPOTIFY_DEFAULT_PLAYLIST_ID) \
      .first()
    session.close()
    return result


  def insert_spotify_tracks(self, track_ids):
    for track_id in track_ids:
      if self.get_spotify_track(track_id) is None:
        self.insert_spotify_track(track_id)


  def insert_spotify_track(self, track_id, user_id=None):
    s = self.Session()
    try:
      s.add(SpotifyTrack(
        external_track_id=track_id,
        external_playlist_id=SPOTIFY_DEFAULT_PLAYLIST_ID,
        create_slack_user_id=user_id
      ))
      s.commit()
    except IntegrityError:
      print "Unable to add duplicate track " + track_id
    finally:
      s.close()



class SpotifyTrack(Base):
  __tablename__ = 'spotify_track'
  spotify_track_id = Column(Integer, primary_key=True)
  external_playlist_id = Column(String(20))
  external_track_id = Column(String(20))
  create_slack_user_id = Column(String(20))
  create_time = Column(TIMESTAMP)
