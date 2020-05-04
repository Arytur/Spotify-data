from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from .api_endpoints import save_access_token_to_client_session
from .decorators import token_validation
from .selectors import (
    get_album_details,
    get_albums_table,
    get_track_details,
    get_tracks_table,
)
from .tasks import (
    get_artist_and_albums,
    get_new_releases,
    get_search_results,
    get_user_recently_played
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
        ctx = get_track_details(request, track_id)
        return render(request, "track.html", ctx)


class TracksTableView(View):
    """
    Display table with all tracks saved in the  db.
    """

    def get(self, request):
        ctx = get_tracks_table()
        return render(request, "tracks_table.html", ctx)


@method_decorator(token_validation, name="dispatch")
class AlbumDetailView(View):
    """
    Display collected info about album.
    image, tracks, features.
    """

    def get(self, request, album_id):
        ctx = get_album_details(request, album_id)
        return render(request, "album.html", ctx)


class AlbumTableView(View):
    """
    Display table with all albums saved in the  db.
    """

    def get(self, request):
        ctx = get_albums_table()
        return render(request, "albums_table.html", ctx)


@method_decorator(token_validation, name="dispatch")
class ArtistDetailView(View):
    """
    Display a list with all artist's albums
    """
    def get(self, request, artist_id):
        artist, albums = get_artist_and_albums(request, artist_id)
        ctx = {"artist": artist, 'albums': albums}
        return render(request, "artist.html", ctx)


@method_decorator(token_validation, name="dispatch")
class SearchView(View):
    """
    Display a list of artists that matches searching word.
    """
    def get(self, request):
        searching = request.GET.get("q")
        result_list, total = get_search_results(request, searching)
        ctx = {
            'searching': searching,
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
