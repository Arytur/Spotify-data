import requests

from .api_endpoints import API_ENDPOINTS, PLAYLISTS_URI


def get_access_token(request):
    return request.session.get("access_token")


class SpotifyRequest:
    def __init__(self, request):
        self.access_token = get_access_token(request)
        self.authorization_header = {
            "Authorization": "Bearer {}".format(self.access_token)
        }

    def _requests_url(self, url):
        resp = requests.get(url, headers=self.authorization_header)
        return resp.json()

    def get_user_recently_played(self):
        url = API_ENDPOINTS["user_recently_played"]
        resp = self._requests_url(url)
        return resp["items"]

    def get_new_releases(self):
        url = API_ENDPOINTS["new_releases"]
        resp = self._requests_url(url)
        return resp["albums"]["items"]

    def get_album(self, album_id):
        url = API_ENDPOINTS["album"] + album_id
        resp = self._requests_url(url)
        return resp

    def get_track(self, track_id):
        url = API_ENDPOINTS["track"] + track_id
        resp = self._requests_url(url)
        return resp

    def get_spotify_playlists(self):

        playlists_resp = {}
        for k, v in PLAYLISTS_URI.items():
            url = (
                API_ENDPOINTS["spotify_playlists"][0]
                + v
                + API_ENDPOINTS["spotify_playlists"][1]
            )
            resp = self._requests_url(url)
            playlists_resp[k] = resp

        return playlists_resp

    def get_playlist_tracks(self, playlist_id):
        url = (
            API_ENDPOINTS["playlist_track"][0]
            + playlist_id
            + API_ENDPOINTS["playlist_track"][1]
        )
        return self._requests_url(url)

    def get_track_audio_features(self, track_id):
        url = API_ENDPOINTS["track_audio_feature"] + track_id
        return self._requests_url(url)

    def search_result(self, searching):
        url = API_ENDPOINTS["search"][0] + searching + API_ENDPOINTS["search"][1]
        return self._requests_url(url)

    def artist_albums(self, artist):
        url = (
            API_ENDPOINTS["artist_albums"][0]
            + artist
            + API_ENDPOINTS["artist_albums"][1]
        )
        return self._requests_url(url)

