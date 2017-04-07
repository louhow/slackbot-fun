from slackbot.bot import listen_to
from slackbot.bot import respond_to
from core.helpers.common import spotify_api

@listen_to("\<.*https://open.spotify.com/track/(.*)\s*\>")
def listen_add_track(message, track_id):
    __add_track(message, track_id)


@respond_to("\<.*https://open.spotify.com/track/(.*)\s*\>")
def respond_add_track(message, track_id):
    __add_track(message, track_id)


def __add_track(message, track_id):
    message.reply_webapi(spotify_api.add_track(track_id))
