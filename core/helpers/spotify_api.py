import base64
import json
import random
import requests
import spotipy
from spotipy.client import SpotifyException

class Spotify_Api(object):
    def __init__(self, client_id, client_secret, user_name, user_refresh_token, default_playlist_id):
        self.user_name = user_name
        self.file = "spotify_access_token.txt"
        self.token_path = "https://accounts.spotify.com/api/token"
        self.failure_messages = [
            "This track is old news. Boo this man!",
            "Shame bell this reposter!",
            "Don't worry, I won't tell anybody you re-posted",
            "It seems like somebody has added this track already",
            "Nobody likes a copycat",
            "Get your own style man, this track has already been added.",
            "It's not a big deal that you just REPOSTED."
        ]
        self.success_messages = [
            "Track added!",
            "Acknowledged.",
            "Roger that.",
            "10-4, Ghost Rider.",
            "I gotchu mayne",
            "Put it in the books!",
            "Awww yeah, track added."
        ]

        self.playlist_id = default_playlist_id # The Thread
        auth_header = base64.b64encode(str(client_id + ':' + client_secret).encode())
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + auth_header.decode()
        }
        self.data = {
            'grant_type': 'refresh_token',
            'refresh_token': user_refresh_token
        }

    def add_track(self, track):
        # TODO Use fancy schmancy decorators...or somethin'
        if self.make_spotify_call(self.__track_exists, track):
            return random.choice(self.failure_messages)

        self.make_spotify_call(self.__attempt_add_track, track)
        return random.choice(self.success_messages)

    def __attempt_add_track(self, track):
        sp = spotipy.Spotify(auth=self.__get_access_token())
        sp.user_playlist_add_tracks(self.user_name, self.playlist_id, [track])

    def __refresh_access_token(self):
        print("Refreshing access token")
        new_access_token = self.__create_new_access_token()
        self.__save_access_token(new_access_token)
        return new_access_token

    def __get_access_token(self):
        print("Fetching access token")
        f = open(self.file, 'r')
        access_token = f.read()
        f.close()
        return access_token if access_token else 'dummy_token'

    def __create_new_access_token(self):
        response = requests.post(
            self.token_path,
            headers=self.headers,
            data=self.data)

        data = json.loads(response.text)

        return data['access_token']

    def __save_access_token(self, new_access_token):
        f = open(self.file, 'w')
        f.write(new_access_token)
        f.close()

    def __get_nerd_word(self):
        return random.choice(self.nerd_words)

    def __track_exists(self, track_id):
        current_tracks = self.__fetch_tracks()

        return len([track for track in current_tracks if track['track']['id'] == track_id]) > 0

    def __fetch_tracks(self):
        sp = spotipy.Spotify(auth=self.__get_access_token())
        response = sp.user_playlist(
                self.user_name,
                self.playlist_id,
                # fields='tracks.items(track(name,id,album(name,href),artists(id,name)))')
                fields='tracks.items(track(id))')

        return response['tracks']['items']

    def make_spotify_call(self, f, *args, **kwargs):
        try:
            return f(*args, **kwargs)
        except SpotifyException as e:
            if e.http_status != 401:
                raise

            self.__refresh_access_token()
            return f(*args, **kwargs)


