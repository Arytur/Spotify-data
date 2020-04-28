import logging
import requests

from .api_endpoints import API_ENDPOINTS

LOG = logging.getLogger(__name__)

# TODO: create nice docs


def requests_url(request, url):
    access_token = request.session.get("access_token")
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}
    resp = requests.get(url, headers=authorization_header)
    return resp.json()


def get_new_releases(request):  # pragma: no cover
    url = API_ENDPOINTS["new_releases"]
    results = requests_url(request, url)
    return results["albums"]["items"]


def get_user_recently_played(request):  # pragma: no cover
    url = API_ENDPOINTS["user_recently_played"]
    results = requests_url(request, url)
    return results["items"]["track"]


def get_album(request, album_id):  # pragma: no cover
    url = API_ENDPOINTS["album"] + album_id
    return requests_url(request, url)


def get_track(request, track_id):  # pragma: no cover
    url = API_ENDPOINTS["track"] + track_id
    return requests_url(request, url)


def get_track_audio_features(request, track_id):  # pragma: no cover
    url = API_ENDPOINTS["track_audio_feature"] + track_id
    return requests_url(request, url)


def get_search_results(request, searching):  # pragma: no cover
    url = API_ENDPOINTS["search"][0] + searching + API_ENDPOINTS["search"][1]
    results = requests_url(request, url)
    artists = results['artists']['items']
    found_total = results['artists']['total']
    return artists, found_total


def get_artist(request, artist_id):  # pragma: no cover
    url = API_ENDPOINTS['artist'] + artist_id
    return requests_url(request, url)


def get_artist_and_albums(request, artist_id):  # pragma: no cover
    url = API_ENDPOINTS["artist_albums"][0] + artist_id + API_ENDPOINTS["artist_albums"][1]
    artist_name = get_artist(request, artist_id)['name']
    results = requests_url(request, url)
    return artist_name, results["items"]
