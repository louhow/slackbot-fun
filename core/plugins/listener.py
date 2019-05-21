from common import spotify_api, dao
from slackbot.bot import listen_to
from slackbot.bot import respond_to
from spotipy.client import SpotifyException
from core.helpers import slack_client
import re
import random

failure_messages = [
    "This track is old news. Boo this man!",
    "Shame bell this reposter!",
    "Don't worry, I won't tell anybody you re-posted.",
    "It seems like somebody has added this track already.",
    "Nobody likes a copycat.",
    "Get your own style man, this track has already been added.",
    "It's not a big deal that you just REPOSTED."
]
success_messages = [
    "Track added!",
    "Acknowledged.",
    "Roger that.",
    "10-4, Ghost Rider.",
    "I gotchu mayne",
    "Put it in the books!",
    "Awww yeah, track added."
]


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
            spotify_track = dao.get_spotify_track(track_id)

            if spotify_track is None:
                spotify_api.add_track(track_id)
                dao.insert_spotify_track(track_id, slack_client.get_user_id(message))
                message.reply_webapi(random.choice(success_messages))
            else:
                fail_msg = random.choice(failure_messages) + " This was added at or before " + str(spotify_track.create_time.date()) + "."
                if spotify_track.create_slack_user_id is not None:
                    display_name = slack_client.get_display_name_for_user_id(spotify_track.create_slack_user_id)
                    fail_msg += " Credit to @" + display_name
                message.reply_webapi(fail_msg)
        except SpotifyException as e:
            message.reply_webapi(e.msg)

# Hacky, but slackbot is refusing to group match on '\w+' - so we'll just parse this out ourselves
# Must match on the following cases:
#   path = 15YhdGDim13g3hB1NOYU5k?si=HNfOC5jfTD2t3ohnJowoRg
#   path = 15YhdGDim13g3hB1NOYU5k
def __get_track_id(path):
    return re.search('\w+', path).group()