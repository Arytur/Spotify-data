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


def get_artist(request, artist_id):
    url = API_ENDPOINTS['artist'] + artist_id
    return requests_url(request, url)


def get_artist_and_albums(request, artist_id):
    url = API_ENDPOINTS["artist_albums"][0] + artist_id + API_ENDPOINTS["artist_albums"][1]
    artist_name = get_artist(request, artist_id)['name']
    results = requests_url(request, url)
    return artist_name, results["items"]


# CREATE

def create_artist(resp):
    artist, _ = Artist.objects.get_or_create(
        id=resp["artists"][0]["id"], name=resp["artists"][0]["name"]
    )
    return artist


def create_track(request, track_id):
    track_data = get_track(request, track_id)
    artist = create_artist(track_data)
    track = Track.objects.create(id=track_id, artist=artist, name=track_data["name"])
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
        tr_feat = track.trackfeatures_set.get()
        feat = tr_feat.features.get_features
        for key in feat.keys():
            dict_of_features[key].append(feat[key])

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


def create_tracks_from_album(request, album_data):

    tracks_list = []
    for item in album_data["tracks"]["items"]:
        try:
            track = Track.objects.get(id=item["id"])
        except Track.DoesNotExist:
            track = create_track_and_features(request, item["id"])
        tracks_list.append(track)
    return tracks_list


def create_album(request, album_id):
    album_data = get_album(request, album_id)
    artist = create_artist(album_data)
    album = Album.objects.create(
        id=album_data['id'],
        name=album_data["name"],
        artist=artist,
        image=album_data["images"][1]["url"],
    )
    return album, album_data


def create_album_tracks_and_features(request, album_id):

    album, album_data = create_album(request, album_id)
    tracks_list = create_tracks_from_album(request, album_data)
    album.tracks.add(*tracks_list)

    create_album_features(tracks_list, album)
    return album
