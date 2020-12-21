import base64
import json
import os
import requests
import spotipy


class SpotifyApi(object):
    def __init__(self,
                 client_id, client_secret, user_name, user_refresh_token,
                 default_playlist_id):
        self.user_name = user_name
        self.playlist_id = default_playlist_id
        self.spotify = spotipy.Spotify(
            auth_manager=SpotifyAuthManager(client_id, client_secret, user_refresh_token))

    def add_track(self, track):
        self.spotify.user_playlist_add_tracks(self.user_name, self.playlist_id, [track])

    def fetch_track_ids(self):
        tracks = []
        offset = 0
        while True:
            print('Fetching playlist %s from offset %s' % (self.playlist_id, offset))
            response = self.spotify.user_playlist_tracks(
                user=self.user_name,
                playlist_id=self.playlist_id,
                # fields='tracks.items(track(name,id,album(name,href),artists(id,name)))')
                fields='items(track(id))',
                limit=100,  # Max is 100
                offset=offset
            )

            offset += 100
            new_track_ids = list(map(lambda item: item['track']['id'], response['items']))
            tracks = tracks + new_track_ids
            if len(new_track_ids) < 100:
                print('Found %d tracks' % (len(tracks)))
                return tracks


class SpotifyAuthManager:
    def __init__(self, client_id, client_secret, user_refresh_token):
        self.file = os.path.dirname(__file__) + "/spotify_access_token.txt"
        auth_header = base64.b64encode(str(client_id + ':' + client_secret).encode())
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + auth_header.decode()
        }
        self.data = {
            'grant_type': 'refresh_token',
            'refresh_token': user_refresh_token
        }

    def get_access_token(self):
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers=self.headers,
            data=self.data)

        data = json.loads(response.text)

        return data['access_token']
