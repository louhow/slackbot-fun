from core.helpers.common import spotify_api
from slackbot.bot import listen_to
from slackbot.bot import respond_to
from spotipy.client import SpotifyException
import re

@listen_to("\<.*https://open.spotify.com/track/(.*)\s*\>")
def listen_add_track(message, path):
    __add_track(message, path)

@respond_to("\<.*https://open.spotify.com/track/(.*)\s*\>")
def respond_add_track(message, path):
    __add_track(message, path)

def __add_track(message, path):
    if "skip" in message._body['text']:
        message.reply_webapi("No worries, I won't add this one.")
    else:
        try:
            track_id = __get_track_id(path)
            message.reply_webapi(spotify_api.add_track(track_id))
        except SpotifyException as e:
            message.reply_webapi(e.msg)

# Hacky, but slackbot is refusing to group match on '\w+' - so we'll just parse this out ourselves
# Must match on the following cases:
#   path = 15YhdGDim13g3hB1NOYU5k?si=HNfOC5jfTD2t3ohnJowoRg
#   path = 15YhdGDim13g3hB1NOYU5k
def __get_track_id(path):
    return re.search('\w+', path).group()