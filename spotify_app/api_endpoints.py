# Authentication Steps, parameters, and responses are defined at
# https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response.
import base64
import json
import os

import requests

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


# API Credentials
mykeys_file = os.path.join(settings.BASE_DIR, "mykeys.json")
load_keys = json.load(open(mykeys_file, "r+"))
client_id, client_secret = load_keys['id'], load_keys['secret']
if settings.SETTINGS_MODULE != 'settings.test_settings':  # pragma: no cover
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
def user_context(request):  # pragma: no cover
    ctx = {"url_args": url_args, "auth_url": auth_url}
    return ctx


def save_access_token_to_client_session(request):

    # get token from URL
    auth_token = request.GET.get("code")

    code_payload = {
        "grant_type": "authorization_code",
        "code": auth_token,
        "redirect_uri": REDIRECT_URI,
    }
    headers = {"Authorization": "Basic {}".format(BASE64)}
    post_request = requests.post(
        SPOTIFY_TOKEN_URL, data=code_payload, headers=headers
    )
    response_data = json.loads(post_request.text)

    # save token to session
    request.session["access_token"] = response_data["access_token"]
    request.session["refresh_token"] = response_data["refresh_token"]
    request.session.set_expiry(response_data["expires_in"])


SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)
USER_PROFILE_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, "me")


API_ENDPOINTS = dict(
    [
        # https://api.spotify.com/v1//me/player/recently-played
        (
            "user_recently_played",
            "{}/me/player/recently-played".format(SPOTIFY_API_URL),
        ),
        # https://api.spotify.com/v1/browse/new-releases
        ("new_releases", "{}/{}/{}".format(SPOTIFY_API_URL, "browse", "new-releases")),
        # https://api.spotify.com/v1/albums/{id}
        ("album", "{}/{}/".format(SPOTIFY_API_URL, "albums")),
        # https://api.spotify.com/v1/tracks/{id}
        ("track", "{}/{}/".format(SPOTIFY_API_URL, "tracks")),
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
