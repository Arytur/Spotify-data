import logging
import requests

from .api_endpoints import API_ENDPOINTS, PLAYLISTS_URI

LOG = logging.getLogger(__name__)

def requests_url(request, url):
    access_token = request.session.get("access_token")
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}
    resp = requests.get(url, headers=authorization_header)
    return resp.json()


def get_new_releases(request):
    url = API_ENDPOINTS["new_releases"]
    results = requests_url(request, url)
    return results["albums"]["items"]


def get_user_recently_played(request):
    url = API_ENDPOINTS["user_recently_played"]
    results = requests_url(request, url)
    return results["items"]


def get_album(request, album_id):
    url = API_ENDPOINTS["album"] + album_id
    return requests_url(request, url)


def get_track(request, track_id):
    url = API_ENDPOINTS["track"] + track_id
    return requests_url(request, url)


def get_spotify_playlists(request):

    # TODO: make it work or remove it
    playlists_resp = {}
    for k, v in PLAYLISTS_URI.items():
        url = (
            API_ENDPOINTS["spotify_playlists"][0]
            + v
            + API_ENDPOINTS["spotify_playlists"][1]
        )
        results = requests_url(request, url)
        playlists_resp[k] = results

    return playlists_resp


def get_playlist_tracks(request, playlist_id):
    url = (
        API_ENDPOINTS["playlist_track"][0]
        + playlist_id
        + API_ENDPOINTS["playlist_track"][1]
    )
    return requests_url(request, url)


def get_track_audio_features(request, track_id):
    url = API_ENDPOINTS["track_audio_feature"] + track_id
    return requests_url(request, url)


def get_search_results(request, searching):
    url = API_ENDPOINTS["search"][0] + searching + API_ENDPOINTS["search"][1]
    return requests_url(request, url)


def get_artist_albums(request, artist):
    url = API_ENDPOINTS["artist_albums"][0] + artist + API_ENDPOINTS["artist_albums"][1]
    return requests_url(request, url)
