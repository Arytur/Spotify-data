import json
import base64
import requests

# Authentication Steps, paramaters, and responses are defined at
# https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response.

#  Client Keys
CLIENT = json.load(open('mykeys.json', 'r+'))
CLIENT_ID = CLIENT['id']
CLIENT_SECRET = CLIENT['secret']
BASE64 = base64.b64encode(bytes(CLIENT_ID + ':' + CLIENT_SECRET, 'ascii'))
BASE64 = BASE64.decode('ascii')

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

# Parameters combine in one part
auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}

url_args = "&".join(["{}={}".format(key, val) for key, val in auth_query_parameters.items()])
auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)

# Context to use in authorizations/callback
def user_context(request):
    ctx = {
        'url_args': url_args,
        'auth_url': auth_url
    }
    return ctx

USER_PROFILE_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'me')
USER_RECENTLY_PLAYED_ENDPOINT = "{}/{}/{}".format(USER_PROFILE_ENDPOINT,
                                                  'player', 'recently-played')
NEW_RELEASES_ENDPOINT = "{}/{}/{}".format(SPOTIFY_API_URL, 'browse', 'new-releases')