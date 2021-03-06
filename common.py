from core.helpers.help import HelpText
from core.helpers.spotify_api import SpotifyApi
from slackbot_settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_USER_NAME, SPOTIFY_REFRESH_TOKEN, SPOTIFY_DEFAULT_PLAYLIST_ID
from slackbot.bot import Bot
from core.helpers.dao import Dao


spotify_api = SpotifyApi(
    SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET,
    SPOTIFY_USER_NAME, SPOTIFY_REFRESH_TOKEN,
    SPOTIFY_DEFAULT_PLAYLIST_ID)

help_text = HelpText()
bot = Bot()
bot_slack_client = bot._client
dao = Dao()

track_ids = spotify_api.fetch_track_ids()
dao.insert_spotify_tracks(track_ids)


def get_user_id(message):
    return message._body['user']
