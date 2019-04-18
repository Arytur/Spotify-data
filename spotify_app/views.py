from django.shortcuts import render, redirect
from django.views import View
from .user_data_context import *
import requests
import json
from .models import Track, Album
from .tasks import get_access_token


class Index(View):

    def get(self, request):
        if 'access_token' not in request.session:
            return redirect('callback')

        access_token = get_access_token(request)
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}

        new_releases = get_new_releases(authorization_header)
        new_releases = new_releases['albums']['items']

        return render(request, 'main.html', {'new_releases': new_releases})


class Callback(View):

    def get(self, request):
        if 'code' in request.GET:

            # get token from URL
            auth_token = request.GET.get('code')

            code_payload = {
                "grant_type": "authorization_code",
                "code": auth_token,
                "redirect_uri": REDIRECT_URI
            }
            headers = {"Authorization": "Basic {}".format(BASE64)}
            post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)
            response_data = json.loads(post_request.text)

            # save token to session
            request.session['access_token'] = response_data["access_token"]
            request.session['refresh_token'] = response_data["refresh_token"]
            request.session.set_expiry(response_data["expires_in"])

            return redirect('/')
        else:
            return render(request, 'callback.html')


class UserRecentlyPlayedView(View):

    def get(self, request):
        if 'access_token' not in request.session:
            return redirect('callback')
        
        access_token = get_access_token(request)
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}

        recently_played = get_users_recently_played(authorization_header)
        recently_played = recently_played['items']
        return render(request, 'recently_played.html', {'recently_played': recently_played})


class AlbumView(View):

    def get(self, request, album_id):
        if 'access_token' not in request.session:
            return redirect('callback')
        
        access_token = get_access_token(request)
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}

        album = get_album(authorization_header, album_id)
        tracks = album['tracks']['items']

        if Album.objects.filter(album_id=album_id).exists():
            spot_album = Album.objects.get(album_id=album_id)
        else:
            try:
                tracks_number = len(tracks)
                dict_track = {'danceability': [], 'speechiness': [], 'acousticness': [],
                              'valence': [], 'instrumentalness': [], 'energy': [], 'liveness': []}
                for track in tracks:
                    track = get_track_audio_features(authorization_header, track['id'])
                    dict_track['danceability'].append(float(format(track['danceability'], '.3f')))
                    dict_track['speechiness'].append(float(format(track['speechiness'], '.3f')))
                    dict_track['acousticness'].append(float(format(track['acousticness'], '.3f')))
                    dict_track['valence'].append(float(format(track['valence'], '.3f')))
                    dict_track['instrumentalness'].append(float(format(track['instrumentalness'], '.3f')))
                    dict_track['energy'].append(float(format(track['energy'], '.3f')))
                    dict_track['liveness'].append(float(format(track['liveness'], '.3f')))

                spot_album = Album.objects.create(album_id=album_id, album_artist=album['artists'][0]['name'],
                                                album_name=album['name'],
                                                danceability=float(format(sum(dict_track['danceability']) / tracks_number, '.3f')),
                                                speechiness=float(format(sum(dict_track['speechiness']) / tracks_number, '.3f')),
                                                acousticness=float(format(sum(dict_track['acousticness']) / tracks_number, '.3f')),
                                                valence=float(format(sum(dict_track['valence']) / tracks_number, '.3f')),
                                                instrumentalness=float(format(sum(dict_track['instrumentalness']) / tracks_number, '.3f')),
                                                energy=float(format(sum(dict_track['energy']) / tracks_number, '.3f')),
                                                liveness=float(format(sum(dict_track['liveness']) / tracks_number, '.3f')))

            except KeyError:
                ctx = {
                    'album': album,
                    'tracks': tracks
                }
                return render(request, 'album.html', ctx)
        album_avg = [
            int(spot_album.danceability * 100),
            int(spot_album.speechiness * 100),
            int(spot_album.acousticness * 100),
            int(spot_album.valence * 100),
            int(spot_album.instrumentalness * 100),
            int(spot_album.energy * 100),
            int(spot_album.liveness * 100)]

        ctx = {
            'album': album,
            'tracks': tracks,
            'spot_album': spot_album,
            'album_avg': album_avg
        }
        return render(request, 'album.html', ctx)


class SpotifyPlaylistsView(View):


    def get(self, request):
        if 'access_token' not in request.session:
            return redirect('callback')

        access_token = get_access_token(request)
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}

        # playlist from different decades
        sixties = get_spotify_playlist(authorization_header, '37i9dQZF1DWYoG7spxcDsi')
        seventies = get_spotify_playlist(authorization_header, '37i9dQZF1DX5vi6QexgFgr')
        eighties = get_spotify_playlist(authorization_header, '37i9dQZF1DWWC8p2yKdFrw')
        nineties = get_spotify_playlist(authorization_header, '37i9dQZF1DX1leCUq7he50')
        twentyzero = get_spotify_playlist(authorization_header, '37i9dQZF1DX5qXEz970M38')
        twentyten = get_spotify_playlist(authorization_header, '37i9dQZF1DX7bSIS915wSM')
        ctx = {
            'sixties': sixties,
            'seventies': seventies,
            'eighties': eighties,
            'nineties': nineties,
            'twentyzero': twentyzero,
            'twentyten': twentyten
        }
        return render(request, 'spotify_playlists.html', ctx)


class PlaylistView(View):

    def get(self, request, playlist_id):
        if 'access_token' not in request.session:
            return redirect('callback')

        access_token = get_access_token(request)
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}
        
        playlist_tracks = get_playlist_tracks(authorization_header, playlist_id)
        feature_track = []
        for track in playlist_tracks['items']:
            feature_track.append(track['track']['id'])
        ctx = {
            'playlist_tracks': playlist_tracks,
            'feature_track': feature_track
        }
        return render(request, 'playlist.html', ctx)


class TrackAudioFeaturesView(View):

    def get(self, request, track_id, track_artist, track_name):
        if 'access_token' not in request.session:
            return redirect('callback')

        access_token = get_access_token(request)
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}

        track = get_track_audio_features(authorization_header, track_id)
        if Track.objects.filter(track_id=track_id).exists():
            spot_track = Track.objects.get(track_id=track_id)
        else:
            spot_track = Track.objects.create(track_id=track_id,
                                              track_artist=track_artist,
                                              track_name=track_name,
                                              danceability=float(format(track['danceability'], '.3f')),
                                              speechiness=float(format(track['speechiness'], '.3f')),
                                              acousticness=float(format(track['acousticness'], '.3f')),
                                              valence=float(format(track['valence'], '.3f')),
                                              instrumentalness=float(format(track['instrumentalness'], '.3f')),
                                              energy=float(format(track['energy'], '.3f')),
                                              liveness=float(format(track['liveness'], '.3f')))
        table_track = [
            int(track['danceability'] * 100),
            int(track['speechiness'] * 100),
            int(track['acousticness'] * 100),
            int(track['valence'] * 100),
            int(track['instrumentalness'] * 100),
            int(track['energy'] * 100),
            int(track['liveness'] * 100)]
        ctx = {
            'track': track,
            'spot_track': spot_track,
            'table_track': table_track,
            'track_artist': track_artist,
            'track_name': track_name
        }
        return render(request, 'track.html', ctx)


class TracksTableView(View):

    def get(self, request):
        tracks = Track.objects.all()
        return render(request, 'tracks_table.html', {'tracks': tracks})


class SearchView(View):

    def get(self, request):
        if 'access_token' not in request.session:
            return redirect('callback')

        access_token = get_access_token(request)
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}

        searching = request.GET.get('q')
        result = search_result(authorization_header, searching)
        result_list = result['artists']
        return render(request, 'search.html', {'result_list': result_list})


class ArtistView(View):

    def get(self, request, artist_id):
        if 'access_token' not in request.session:
            return redirect('callback')

        access_token = get_access_token(request)
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}
        
        artist = artist_albums(authorization_header, artist_id)
        return render(request, 'artist.html', {'artist': artist})


class AlbumTableView(View):

    def get(self, request):
        albums = Album.objects.all()
        return render(request, 'albums_table.html', {'albums': albums})


