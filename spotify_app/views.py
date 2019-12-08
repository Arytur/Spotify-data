import json

import requests

from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from .api_endpoints import REDIRECT_URI, BASE64, SPOTIFY_TOKEN_URL
from .decorators import token_validation
from .models import Album, Artist, Features, Track, TrackFeatures
from .tasks import get_access_token, SpotifyRequest


@method_decorator(token_validation, name="dispatch")
class Index(View):
    """
    Display new releases in Spotify.
    """

    def get(self, request):

        spotify = SpotifyRequest(request)
        new_releases = spotify.get_new_releases()

        return render(request, "index.html", {"new_releases": new_releases})


@method_decorator(token_validation, name="dispatch")
class UserRecentlyPlayedView(View):
    def get(self, request):

        spotify = SpotifyRequest(request)
        recently_played = spotify.get_user_recently_played()
        return render(
            request, "recently_played.html", {"recently_played": recently_played}
        )


@method_decorator(token_validation, name="dispatch")
class TrackDetailView(View):
    def get(self, request, track_id):

        try:
            # TODO: Omg, change it...
            track = Track.objects.get(id=track_id)
            track_features = track.trackfeatures_set.first()
            features = track_features.features
            chart_numbers = features.get_features_for_chart
        except Track.DoesNotExist:
            # TODO: move creating it to another file
            spotify = SpotifyRequest(request)
            track_data = spotify.get_track(track_id)

            # TODO: add Artist for a given track
            artist, _ = Artist.objects.get_or_create(
                name=track_data["artists"][0]["name"]
            )
            track_name = track_data["name"]
            track = Track.objects.create(id=track_id, artist=artist, name=track_name)

            features = spotify.get_track_audio_features(track_id)
            features = Features.objects.create(
                danceability=features["danceability"],
                speechiness=features["speechiness"],
                acousticness=features["acousticness"],
                valence=features["valence"],
                instrumentalness=features["instrumentalness"],
                energy=features["energy"],
                liveness=features["liveness"],
            )
            track_feature = TrackFeatures.objects.create(track=track, features=features)
            chart_numbers = features.get_features_for_chart

        ctx = {"track": track, "features": features, "chart": chart_numbers}
        return render(request, "track.html", ctx)


class TracksTableView(View):
    """
    Display table with all tracks collected.
    """

    def get(self, request):
        tracks = Track.objects.all()
        return render(request, "tracks_table.html", {"tracks": tracks})


@method_decorator(token_validation, name="dispatch")
class AlbumDetailView(View):
    """
    Display collected info about album.
    image, tracks, features
    """

    def get(self, request, album_id):

        # TODO: save all track from this album

        try:
            album = Album.objects.get(id=album_id)
        except Album.DoesNotExist:
            spotify = SpotifyRequest(request)
            album_data = spotify.get_album(album_id)
            artist, _ = Artist.objects.get_or_create(
                name=album_data["artists"][0]["name"]
            )
            album = Album.objects.create(
                id=album_id,
                name=album_data["name"],
                artist=artist,
                image=album_data["images"][1]["url"],
            )

            tracks = album_data["tracks"]["items"]

            # TODO: calculate features for album.
            # try:
            #     tracks = album_data["tracks"]["items"]
            #     album_features = Album.calculate_album_features(spotify, tracks)
            # except KeyError:
            #     ctx = {"album": album_data, "tracks": tracks}
            #     return render(request, "album.html", ctx)

            # features = Features.objects.create(
            #     danceability=album_features["danceability"],
            #     speechiness=album_features["speechiness"],
            #     acousticness=album_features["acousticness"],
            #     valence=album_features["valence"],
            #     instrumentalness=album_features["instrumentalness"],
            #     energy=album_features["energy"],
            #     liveness=album_features["liveness"],
            # )
            # AlbumFeatures.objects.create(
            #         album=album,
            #         features=features
            # )

        ctx = {
            "album": album,
            "tracks": tracks,
            # "album_avg": album.get_features_for_chart(),
        }
        return render(request, "album.html", ctx)


class AlbumTableView(View):
    def get(self, request):
        albums = Album.objects.all()
        return render(request, "albums_table.html", {"albums": albums})


@method_decorator(token_validation, name="dispatch")
class ArtistDetailView(View):
    def get(self, request, artist_id):

        spotify = SpotifyRequest(request)

        artist = spotify.artist_albums(artist_id)
        return render(request, "artist.html", {"artist": artist})


@method_decorator(token_validation, name="dispatch")
class SpotifyPlaylistsView(View):
    def get(self, request):

        spotify = SpotifyRequest(request)
        ctx = spotify.get_spotify_playlists()
        return render(request, "spotify_playlists.html", ctx)


@method_decorator(token_validation, name="dispatch")
class PlaylistDetailView(View):
    def get(self, request, playlist_id):

        spotify = SpotifyRequest(request)
        playlist_tracks = spotify.get_playlist_tracks(playlist_id)
        feature_track = [track["track"]["id"] for track in playlist_tracks["items"]]

        ctx = {"playlist_tracks": playlist_tracks}

        return render(request, "playlist.html", ctx)


@method_decorator(token_validation, name="dispatch")
class SearchView(View):
    def get(self, request):

        spotify = SpotifyRequest(request)

        searching = request.GET.get("q")
        result = spotify.search_result(searching)
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
