from common import spotify_api, dao
from slackbot.bot import listen_to
from slackbot.bot import respond_to
from spotipy.client import SpotifyException
from common import get_user_id
import re
import random

failure_messages = [
    "Looks like someone has good taste.",
    "This track has already been added."
]
success_messages = [
    "Track added!",
    "Copy that.",
    "Roger that.",
    "10-4, Ghost Rider.",
    "I gotchu mayne",
    "Put it in the books!",
    "Thank you for using BotBot.",
    "Mmm, that's good music."
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
                if dao.insert_spotify_track(track_id, get_user_id(message)):
                    message.reply_webapi(random.choice(success_messages))
                else:
                    message.reply_webapi("Saving to DB broke (cc lou). Please send again and it should save.")
            else:
                fail_msg = random.choice(failure_messages)
                create_date = str(spotify_track.create_time.date())
                if spotify_track.create_slack_user_id is not None:
                    fail_msg += " This was added on " + create_date + ". Credit to <@" + spotify_track.create_slack_user_id + ">"
                else:
                    fail_msg += " This was added sometime before " + create_date + "."
                message.reply_webapi(fail_msg)
        except SpotifyException as e:
            print(e.msg)
            message.reply_webapi("Talking to Spotify failed (cc lou).")


# Hacky, but slackbot is refusing to group match on '\w+' - so we'll just parse this out ourselves
# Must match on the following cases:
#   path = 15YhdGDim13g3hB1NOYU5k?si=HNfOC5jfTD2t3ohnJowoRg
#   path = 15YhdGDim13g3hB1NOYU5k
def __get_track_id(path):
    return re.search('\w+', path).group()
