import json
import base64
import requests

# Authentication Steps, paramaters, and responses are defined at
# https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response.

#  Client Keys
CLIENT = json.load(open('keys.json', 'r+'))
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

# ------------------ 4. USER RELATED REQUETS  ---------- #


# spotify endpoints
USER_PROFILE_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'me')
USER_PLAYLISTS_ENDPOINT = "{}/{}".format(USER_PROFILE_ENDPOINT, 'playlists')
USER_TOP_ARTISTS_AND_TRACKS_ENDPOINT = "{}/{}".format(
    USER_PROFILE_ENDPOINT, 'top')  # /<type>
USER_RECENTLY_PLAYED_ENDPOINT = "{}/{}/{}".format(USER_PROFILE_ENDPOINT,
                                                  'player', 'recently-played')
BROWSE_FEATURED_PLAYLISTS = "{}/{}/{}".format(SPOTIFY_API_URL, 'browse',
                                              'featured-playlists')
new_releases_endpoint = "{}/{}/{}".format(SPOTIFY_API_URL, 'browse', 'new-releases')


# https://developer.spotify.com/web-api/get-users-profile/
def get_users_profile(auth_header):
    url = USER_PROFILE_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()


# https://developer.spotify.com/web-api/get-a-list-of-current-users-playlists/
def get_users_playlists(auth_header):
    url = USER_PLAYLISTS_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    print(resp.json())
    return resp.json()


# https://developer.spotify.com/web-api/web-api-personalization-endpoints/get-recently-played/
def get_users_recently_played(auth_header):
    url = USER_RECENTLY_PLAYED_ENDPOINT
    resp = requests.get(url, headers=auth_header)
    return resp.json()


# https://developer.spotify.com/web-api/get-list-featured-playlists/
def get_featured_playlists(auth_header):
    url = BROWSE_FEATURED_PLAYLISTS
    resp = requests.get(url, headers=auth_header)
    return resp.json()


def get_new_releases(auth_header):
    url = new_releases_endpoint
    resp = requests.get(url, headers=auth_header)
    return resp.json()


def get_album(auth_header, album_id):
    url = "{}/{}/{}".format(SPOTIFY_API_URL, 'albums', album_id)
    resp = requests.get(url, headers=auth_header)
    return resp.json()


# https://api.spotify.com/v1/users/{user_id}/playlists/{playlist_id}
def get_spotify_playlist(auth_header, playlist_id):
    url = "{}/users/spotify/playlists/{}?market=US".format(SPOTIFY_API_URL, playlist_id)
    resp = requests.get(url, headers=auth_header)
    return resp.json()


def get_playlist_tracks(auth_header, playlist_id):
    url = "{}/users/spotify/playlists/{}/tracks?market=US&limit=50".format(SPOTIFY_API_URL, playlist_id)
    resp = requests.get(url, headers=auth_header)
    return resp.json()


def get_track_audio_features(auth_header, track_id):
    url = "{}/audio-features/{}".format(SPOTIFY_API_URL, track_id)
    resp = requests.get(url, headers=auth_header)
    return resp.json()


def search_result(auth_header, searching):
    url = "{}/search?q={}&type=artist".format(SPOTIFY_API_URL, searching)
    resp = requests.get(url, headers=auth_header)
    return resp.json()


def artist_albums(auth_header, artist):
    url = "{}/artists/{}/albums?album_type=album".format(SPOTIFY_API_URL, artist)
    resp = requests.get(url, headers=auth_header)
    return resp.json()