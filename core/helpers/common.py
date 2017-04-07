from core.helpers.help import HelpText
from core.helpers.spotify_api import Spotify_Api
from slackbot_settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REFRESH_TOKEN, SPOTIFY_DEFAULT_PLAYLIST_ID

spotify_api = Spotify_Api(
    SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REFRESH_TOKEN, SPOTIFY_DEFAULT_PLAYLIST_ID)

help_text = HelpText()