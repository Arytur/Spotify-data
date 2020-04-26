from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from .api_endpoints import save_access_token_to_client_session
from .decorators import token_validation
from .models import Album, AlbumFeatures, Track, TrackFeatures
from .tasks import (
    create_album_tracks_and_features,
    create_track_and_features,
    get_new_releases,
    get_user_recently_played,
    get_search_results,
    get_artist_and_albums,
)


@method_decorator(token_validation, name="dispatch")
class Index(View):
    """
    Display new releases in Spotify.
    """

    def get(self, request):
        new_releases = get_new_releases(request)
        return render(request, "index.html", {"new_releases": new_releases})


@method_decorator(token_validation, name="dispatch")
class UserRecentlyPlayedView(View):
    """
    Display a list with user recently played tracks.
    """

    def get(self, request):
        recently_played_tracks = get_user_recently_played(request)
        return render(
            request, "recently_played.html", {"recently_played_tracks": recently_played_tracks}
        )


@method_decorator(token_validation, name="dispatch")
class TrackDetailView(View):
    """
    Display collected info about track.
    image, features.
    """

    def get(self, request, track_id):

        try:
            track = Track.objects.get(id=track_id)
        except Track.DoesNotExist:
            track = create_track_and_features(request, track_id)

        track_features = track.trackfeatures_set.get()
        features = track_features.features

        chart_numbers = features.get_features_for_chart

        ctx = {"track": track, "features": features, "chart": chart_numbers}
        return render(request, "track.html", ctx)


class TracksTableView(View):
    """
    Display table with all tracks saved in the  db.
    """

    def get(self, request):
        tracks = Track.objects.all()[:10]
        tracks_features = TrackFeatures.objects.filter(track__in=tracks)

        return render(
            request, "tracks_table.html", {"tracks_features": tracks_features}
        )


@method_decorator(token_validation, name="dispatch")
class AlbumDetailView(View):
    """
    Display collected info about album.
    image, tracks, features.
    """

    def get(self, request, album_id):

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
        return render(request, "album.html", ctx)


class AlbumTableView(View):
    """
    Display table with all albums saved in the  db.
    """

    def get(self, request):
        albums = Album.objects.all()[:10]
        albums_features = AlbumFeatures.objects.filter(album__in=albums)
        return render(request, "albums_table.html", {"albums_features": albums_features})


@method_decorator(token_validation, name="dispatch")
class ArtistDetailView(View):
    """
    Display a list with all artist's albums
    """
    def get(self, request, artist_id):
        artist, albums = get_artist_and_albums(request, artist_id)
        return render(request, "artist.html", {"artist": artist, 'albums': albums})


@method_decorator(token_validation, name="dispatch")
class SearchView(View):
    """
    Display a list of artists that matches searching word.
    """
    def get(self, request):
        searching = request.GET.get("q")
        result_list, total = get_search_results(request, searching)
        ctx = {
            'searching':  searching,
            "result_list": result_list,
            'total': total
        }
        return render(request, "search.html", ctx)


class Callback(View):
    """
    View to handle access token in session.
    """
    def get(self, request):
        if "code" in request.GET:
            save_access_token_to_client_session(request)
            return redirect("/")
        else:
            return render(request, "callback.html")
