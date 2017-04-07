from slackbot.bot import listen_to
from slackbot.bot import respond_to
from core.helpers.apis.spotify_api import Spotify_Api

@listen_to("\<.*https://open.spotify.com/track/(.*)\s*\>")
# @listen_to("(.*)")
def listen_add_track(message, track_id):
    __add_track(message, track_id)


@respond_to("\<.*https://open.spotify.com/track/(.*)\s*\>")
# @listen_to("(.*)")
def respond_add_track(message, track_id):
    __add_track(message, track_id)


def __add_track(message, track_id):
    sp = Spotify_Api()
    message.reply_webapi(sp.add_track(track_id))