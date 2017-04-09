import base64
import json
import requests
import spotipy
from spotipy.client import SpotifyException

class Spotify_Api(object):
    def __init__(self, client_id, client_secret, refresh_token, default_playlist_id):
        self.username = "louhow"
        self.file = "spotify_access_token.txt"
        self.tokenPath = "https://accounts.spotify.com/api/token"

        self.playlist_id = default_playlist_id # The Thread
        auth_header = base64.b64encode(str(client_id + ':' + client_secret).encode())
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + auth_header.decode()
        }
        self.data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

    def add_track(self, track):
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
        sp.user_playlist_add_tracks(self.username, self.playlist_id, [track])

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
        return access_token

    def __create_new_access_token(self):
        response = requests.post(
            self.tokenPath,
            headers=self.headers,
            data=self.data)

        data = json.loads(response.text)

        return data['access_token']

    def __save_access_token(self, new_access_token):
        f = open(self.file, 'w')
        f.write(new_access_token)
        f.close()

