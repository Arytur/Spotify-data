import json
import base64

# Authentication Steps, paramaters, and responses are defined at
# https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response.

#  Client Keys
CLIENT_ID = ""
CLIENT_SECRET = ""
BASE64 = 'OWVkN2NmODUwODdhNGMxNzgwYjZkYjAyNjU5YTk5YzM6ZGE4MDllM2NmMjFhNDkwZjg4OThmZjY1YjRkZGQxYmQ='

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)


# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8000
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private user-read-recently-played"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()


auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

url_args = "&".join(["{}={}".format(key, val) for key, val in auth_query_parameters.items()])
auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)


def user_context(request):
    ctx = {
        'url_args': url_args,
        'auth_url': auth_url
    }
    return ctx
