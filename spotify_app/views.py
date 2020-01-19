import json

import requests

from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from .api_endpoints import REDIRECT_URI, BASE64, SPOTIFY_TOKEN_URL
from .decorators import token_validation
from .models import Album, AlbumFeatures, Track, TrackFeatures
from .tasks import (
    create_album_tracks_and_features,
    create_track_and_features,
    get_new_releases,
    get_user_recently_played,
    get_spotify_playlists,
    get_playlist_tracks,
    get_search_results,
    get_artist_albums,
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
    def get(self, request):
        recently_played = get_user_recently_played(request)
        return render(
            request, "recently_played.html", {"recently_played": recently_played}
        )


@method_decorator(token_validation, name="dispatch")
class TrackDetailView(View):
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
    Display table with all tracks collected.
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
    image, tracks, features
    """

    def get(self, request, album_id):

        try:
            album = Album.objects.get(id=album_id)
        except Album.DoesNotExist:
            album = create_album_tracks_and_features(request, album_id)

        album_features = album.albumfeatures_set.get()
        features = album_features.features

        ctx = {
            "album": album,
            "tracks": album.tracks.all(),
            "album_avg": features.get_features_for_chart(),
        }
        return render(request, "album.html", ctx)


class AlbumTableView(View):
    def get(self, request):
        albums = Album.objects.all()[:10]
        albums_features = AlbumFeatures.objects.filter(album__in=albums)
        return render(request, "albums_table.html", {"albums_features": albums_features})


@method_decorator(token_validation, name="dispatch")
class ArtistDetailView(View):
    def get(self, request, artist_id):
        artist = get_artist_albums(request, artist_id)
        return render(request, "artist.html", {"artist": artist})


@method_decorator(token_validation, name="dispatch")
class SpotifyPlaylistsView(View):
    def get(self, request):
        playlists = get_spotify_playlists(request)
        return render(request, "spotify_playlists.html", playlists)


@method_decorator(token_validation, name="dispatch")
class PlaylistDetailView(View):
    def get(self, request, playlist_id):
        playlist_tracks = get_playlist_tracks(request, playlist_id)
        return render(request, {"playlist_tracks": playlist_tracks})


@method_decorator(token_validation, name="dispatch")
class SearchView(View):
    def get(self, request):
        searching = request.GET.get("q")
        result = get_search_results(request, searching)
        result_list = result["artists"]
        return render(request, "search.html", {"result_list": result_list})


class Callback(View):
    def get(self, request):
        if "code" in request.GET:

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

            return redirect("/")
        else:
            return render(request, "callback.html")
