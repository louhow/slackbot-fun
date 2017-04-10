from core.helpers.common import spotify_api
from slackbot.bot import listen_to
from slackbot.bot import respond_to
from spotipy.client import SpotifyException

@listen_to("\<.*https://open.spotify.com/track/(.*)\s*\>")
def listen_add_track(message, track_id):
    __add_track(message, track_id)


@respond_to("\<.*https://open.spotify.com/track/(.*)\s*\>")
def respond_add_track(message, track_id):
    __add_track(message, track_id)


def __add_track(message, track_id):
    try:
        message.reply_webapi(spotify_api.add_track(track_id))
    except SpotifyException as e:
        message.reply_webapi(e.msg)

