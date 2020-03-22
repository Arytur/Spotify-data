# Authentication Steps, parameters, and responses are defined at
# https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response.
import base64
import json
import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


# API Credentials
mykeys_file = os.path.join(settings.BASE_DIR, "mykeys.json")
load_keys = json.load(open(mykeys_file, "r+"))
client_id, client_secret = load_keys['id'], load_keys['secret']
if settings.SETTINGS_MODULE != 'settings.test_settings':
    if client_id == 'your_key' or client_secret == 'your_secret':
        error_msg = 'Set API credentials in mykeys.json'
        raise ImproperlyConfigured(error_msg)

BASE64 = base64.b64encode(bytes(client_id + ":" + client_secret, "ascii"))
BASE64 = BASE64.decode("ascii")

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8000
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private user-read-recently-played"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

# Parameters combine in one part
auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": client_id,
}

url_args = "&".join(
    ["{}={}".format(key, val) for key, val in auth_query_parameters.items()]
)
auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)


# Context to use in authorizations/callback
def user_context(request):
    ctx = {"url_args": url_args, "auth_url": auth_url}
    return ctx


SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)
USER_PROFILE_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, "me")

# playlist from different decades
PLAYLISTS_URI = dict(
    [
        ("sixties", "37i9dQZF1DWYoG7spxcDsi"),
        ("seventies", "37i9dQZF1DX5vi6QexgFgr"),
        ("eighties", "37i9dQZF1DWWC8p2yKdFrw"),
        ("nineties", "37i9dQZF1DX1leCUq7he50"),
        ("twentyzero", "37i9dQZF1DX5qXEz970M38"),
        ("twentyten", "37i9dQZF1DX7bSIS915wSM"),
    ]
)


API_ENDPOINTS = dict(
    [
        # https://developer.spotify.com/web-api/web-api-personalization-endpoints/get-recently-played/
        (
            "user_recently_played",
            "{}/{}/{}".format(USER_PROFILE_ENDPOINT, "player", "recently-played"),
        ),
        # https://api.spotify.com/v1/browse/new-releases
        ("new_releases", "{}/{}/{}".format(SPOTIFY_API_URL, "browse", "new-releases")),
        # https://api.spotify.com/v1/albums/{id}
        ("album", "{}/{}/".format(SPOTIFY_API_URL, "albums")),
        # https://api.spotify.com/v1/tracks/{id}
        ("track", "{}/{}/".format(SPOTIFY_API_URL, "tracks")),
        # https://api.spotify.com/v1/users/{user_id}/playlists/{playlist_id}
        (
            "spotify_playlists",
            ("{}/users/spotify/playlists/".format(SPOTIFY_API_URL), "?market=US"),
        ),
        # https://api.spotify.com/v1/users/{user_id}/playlists/{playlist_id}/tracks
        (
            "playlist_track",
            (
                "{}/users/spotify/playlists/".format(SPOTIFY_API_URL),
                "/tracks?market=US&limit=50",
            ),
        ),
        # https://api.spotify.com/v1/audio-features/{id}
        ("track_audio_feature", "{}/audio-features/".format(SPOTIFY_API_URL)),
        # https://api.spotify.com/v1/search
        ("search", ("{}/search?q=".format(SPOTIFY_API_URL), "&type=artist")),
        # https://api.spotify.com/v1/artists/{id}
        (
            "artist",
            ("{}/artists/".format(SPOTIFY_API_URL)),
        ),
        # https://api.spotify.com/v1/artists/{id}/albums
        (
            "artist_albums",
            ("{}/artists/".format(SPOTIFY_API_URL), "/albums?album_type=album"),
        ),
    ]
)
