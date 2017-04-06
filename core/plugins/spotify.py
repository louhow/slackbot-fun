from slackbot.bot import respond_to
from core.helpers.apis.spotify_api import Spotify_Api

@respond_to("\<.*https://open.spotify.com/track/(.*)\s*\>")
def add_track(message, track_id):
    sp = Spotify_Api()
    message.reply_webapi(sp.add_track(track_id))
