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
        self.nerd_words = ['goob', 'fool', 'dunce', 'noob', 'busta', 'goof', 'dummy', 'silly', 'goober',
                           'nerd', 'dweeb', 'goofball', 'simpleton']

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
        if self.__track_exists(track):
            return 'Nice try, ' + self.__get_nerd_word() + '. That track was already added.'

        # TODO Abstract away shared retry logic
        try:
            self.__attempt_add_track(track)
            return "Successfully added track!"
        except SpotifyException as e:
            if e.http_status == 401:
                self.__refresh_access_token()
                self.__attempt_add_track(track)
                return "Successfully added track!!"
            else:
                return "Failure fetching track '" + track + "': " + e.__str__()

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
        # TODO Abstract away shared retry logic
        try:
            current_tracks = self.__fetch_tracks()
        except SpotifyException as e:
            if e.http_status == 401:
                self.__refresh_access_token()
                current_tracks = self.__fetch_tracks()
            else:
                return False

        # TODO improve this
        current_track_ids = list(map(lambda x: x['track']['id'], current_tracks))
        return len(list(filter(lambda x: x == track_id, current_track_ids))) > 0

    def __fetch_tracks(self):
        sp = spotipy.Spotify(auth=self.__get_access_token())
        response = sp.user_playlist(
                self.user_name,
                self.playlist_id,
                fields='tracks.items(track(name,id,album(name,href),artists(id,name)))')

        return response['tracks']['items']


