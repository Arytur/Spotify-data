import requests
from.api_endpoints import *

def get_access_token(request):
    return request.session.get('access_token')


class SpotifyRequest():

    def __init__(self, request):
        self.access_token = get_access_token(request)
        self.authorization_header = {"Authorization": "Bearer {}".format(self.access_token)}

    # https://developer.spotify.com/web-api/web-api-personalization-endpoints/get-recently-played/
    def get_users_recently_played(self):
        url = USER_RECENTLY_PLAYED_ENDPOINT
        resp = requests.get(url, headers=self.authorization_header)
        return resp.json()

    # https://api.spotify.com/v1/browse/new-releases
    def get_new_releases(self):
        url = NEW_RELEASES_ENDPOINT
        resp = requests.get(url, headers=self.authorization_header)
        return resp.json()

    # https://api.spotify.com/v1/albums/{id}
    def get_album(self, album_id):
        url = "{}/{}/{}".format(SPOTIFY_API_URL, 'albums', album_id)
        resp = requests.get(url, headers=self.authorization_header)
        return resp.json()

    # https://api.spotify.com/v1/users/{user_id}/playlists/{playlist_id}
    def get_spotify_playlist(self, playlist_id):
        url = "{}/users/spotify/playlists/{}?market=US".format(SPOTIFY_API_URL, playlist_id)
        resp = requests.get(url, headers=self.authorization_header)
        return resp.json()

    # https://api.spotify.com/v1/users/{user_id}/playlists/{playlist_id}/tracks
    def get_playlist_tracks(self, playlist_id):
        url = "{}/users/spotify/playlists/{}/tracks?market=US&limit=50".format(SPOTIFY_API_URL, playlist_id)
        resp = requests.get(url, headers=self.authorization_header)
        return resp.json()

    # https://api.spotify.com/v1/audio-features/{id}
    def get_track_audio_features(self, track_id):
        url = "{}/audio-features/{}".format(SPOTIFY_API_URL, track_id)
        resp = requests.get(url, headers=self.authorization_header)
        return resp.json()

    # https://api.spotify.com/v1/search
    def search_result(self, searching):
        url = "{}/search?q={}&type=artist".format(SPOTIFY_API_URL, searching)
        resp = requests.get(url, headers=self.authorization_header)
        return resp.json()

    # https://api.spotify.com/v1/artists/{id}/albums
    def artist_albums(self, artist):
        url = "{}/artists/{}/albums?album_type=album".format(SPOTIFY_API_URL, artist)
        resp = requests.get(url, headers=self.authorization_header)
        return resp.json()
