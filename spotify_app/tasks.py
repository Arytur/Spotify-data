from collections import defaultdict
import logging
import requests

from .api_endpoints import API_ENDPOINTS, PLAYLISTS_URI
from .models import Album, AlbumFeatures, Artist, Features, Track, TrackFeatures

LOG = logging.getLogger(__name__)


def requests_url(request, url):
    access_token = request.session.get("access_token")
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}
    resp = requests.get(url, headers=authorization_header)
    return resp.json()


# GET

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


# CREATE


def create_track(request, track_id):
    track_data = get_track(request, track_id)
    artist, _ = Artist.objects.get_or_create(
        id=track_data["artists"][0]["id"], name=track_data["artists"][0]["name"]
    )
    track_name = track_data["name"]
    track = Track.objects.create(id=track_id, artist=artist, name=track_name)
    return track


def create_track_audio_features(request, track):
    features = get_track_audio_features(request, track.id)
    track_features = Features.objects.create(
        danceability=features["danceability"],
        speechiness=features["speechiness"],
        acousticness=features["acousticness"],
        valence=features["valence"],
        instrumentalness=features["instrumentalness"],
        energy=features["energy"],
        liveness=features["liveness"],
    )
    TrackFeatures.objects.create(track=track, features=track_features)
    return track_features


def create_track_and_features(request, track_id):

    track = create_track(request, track_id)
    create_track_audio_features(request, track)
    return track


def create_album_features(tracks, album):
    dict_of_features = defaultdict(list)
    tracks_number = len(tracks)

    for track in tracks:
        tr_feat = track.get_features
        for key in tr_feat.keys():
            dict_of_features[key].append(tr_feat[key])

    for key in dict_of_features.keys():
        dict_of_features[key] = sum(dict_of_features[key]) / tracks_number

    album_features = Features.objects.create(
        danceability=dict_of_features["danceability"],
        speechiness=dict_of_features["speechiness"],
        acousticness=dict_of_features["acousticness"],
        valence=dict_of_features["valence"],
        instrumentalness=dict_of_features["instrumentalness"],
        energy=dict_of_features["energy"],
        liveness=dict_of_features["liveness"],
    )
    AlbumFeatures.objects.create(album=album, features=album_features)
    return album_features


def create_album_and_features(request, album_id):

    album_data = get_album(request, album_id)
    artist, _ = Artist.objects.get_or_create(
        id=album_data["artists"][0]["id"], name=album_data["artists"][0]["name"]
    )
    album = Album.objects.create(
        id=album_id,
        name=album_data["name"],
        artist=artist,
        image=album_data["images"][1]["url"],
    )
    tracks_features_list = []
    for item in album_data["tracks"]["items"]:
        # TODO use create_track_and_features
        # TODO bulk add all tracks to album
        track, _ = Track.objects.get_or_create(
            id=item["id"], name=item["name"], artist=artist
        )
        album.tracks.add(track)
        track_features = create_track_audio_features(request, track)
        tracks_features_list.append(track_features)

    create_album_features(tracks_features_list, album)
    return album
