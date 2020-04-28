from .models import (
    Album,
    AlbumFeatures,
    Track,
    TrackFeatures
)
from .services import (
    create_album_tracks_and_features,
    create_track_and_features
)


def get_album_details(request, album_id):

    try:
        album = Album.objects.get(id=album_id)
    except Album.DoesNotExist:
        album = create_album_tracks_and_features(request, album_id)

    album_features = album.albumfeatures_set.get()
    features = album_features.features

    chart_numbers = features.get_features_for_chart()

    ctx = {
        "album": album,
        "tracks": album.tracks.all(),
        "features": features,
        "chart": chart_numbers,
    }
    return ctx


def get_albums_table():

    albums = Album.objects.all()[:10]
    albums_features = AlbumFeatures.objects.filter(album__in=albums)
    ctx = {"albums_features": albums_features}
    return ctx


def get_track_details(request, track_id):

    try:
        track = Track.objects.get(id=track_id)
    except Track.DoesNotExist:
        track = create_track_and_features(request, track_id)

    track_features = track.trackfeatures_set.get()
    features = track_features.features
    chart_numbers = features.get_features_for_chart
    ctx = {
        "track": track,
        "features": features,
        "chart": chart_numbers
    }
    return ctx


def get_tracks_table():

    tracks = Track.objects.all()[:10]
    tracks_features = TrackFeatures.objects.filter(track__in=tracks)
    ctx = {"tracks_features": tracks_features}
    return ctx


