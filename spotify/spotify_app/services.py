from collections import defaultdict
from typing import Any, Dict, List, Tuple

from django.db.models.query import QuerySet
from requests.models import Request

from .models import (
    Album,
    AlbumFeatures,
    Artist,
    Features,
    Track,
    TrackFeatures
)
from .tasks import (
    get_album,
    get_track,
    get_track_audio_features
)


def get_or_create_artist(resp):
    artist, _ = Artist.objects.get_or_create(
        id=resp["artists"][0]["id"], name=resp["artists"][0]["name"]
    )
    return artist


def create_track(request: Request, track_id: str) -> Track:
    track_data = get_track(request, track_id)
    artist = get_or_create_artist(track_data)
    track = Track.objects.create(id=track_id, artist=artist, name=track_data["name"])
    return track


def create_track_audio_features(request: Request, track: Track) -> Features:
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


def create_track_and_features(request: Request, track_id: str) -> Track:

    track = create_track(request, track_id)
    create_track_audio_features(request, track)
    return track


def create_album_features(tracks: List[Track], album: Album) -> Features:

    dict_of_features = defaultdict(list)
    tracks_number = len(tracks)

    for track in tracks:
        tr_feat = TrackFeatures.objects.get(track=track)
        feat = tr_feat.features.get_features
        for key in feat.keys():
            dict_of_features[key].append(feat[key])

    for key in dict_of_features:
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


def create_tracks_from_album(request: Request,
                             album_data: Dict[str, Any]) -> List[Track]:

    tracks_list = []
    for item in album_data["tracks"]["items"]:
        try:
            track = Track.objects.get(id=item["id"])
        except Track.DoesNotExist:
            track = create_track_and_features(request, item["id"])
        tracks_list.append(track)
    return tracks_list


def create_album(request: Request, album_id: str) -> Tuple[Album, Dict[str, Any]]:
    album_data = get_album(request, album_id)
    artist = get_or_create_artist(album_data)
    album = Album.objects.create(
        id=album_data['id'],
        name=album_data["name"],
        artist=artist,
        image=album_data["images"][1]["url"],
    )
    return album, album_data


def create_album_tracks_and_features(request: Request, album_id: str) -> Album:

    album, album_data = create_album(request, album_id)
    tracks_list = create_tracks_from_album(request, album_data)
    album.tracks.add(*tracks_list)

    create_album_features(tracks_list, album)
    return album
