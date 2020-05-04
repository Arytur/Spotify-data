from decimal import Decimal
import random
from unittest.mock import Mock, patch

import responses

from django.test import RequestFactory, TestCase

from spotify_app.api_endpoints import API_ENDPOINTS
from spotify_app import tasks
from spotify_app import services
from spotify_app.models import (
    Album,
    AlbumFeatures,
    Artist,
    Features,
    Track,
    TrackFeatures
)
from spotify_app.services import (
    create_album,
    create_album_features,
    create_album_tracks_and_features,
    create_tracks_from_album,
    create_track,
    create_track_audio_features,
    create_track_and_features,
    get_or_create_artist,
)
from spotify_app.tasks import requests_url
from .factories import (
    AlbumFactory,
    FeaturesFactory,
    TrackFactory,
    TrackFeaturesFactory
)


def get_request_factory_with_session():
    request_factory = RequestFactory()
    access_token = '12345'
    request_factory.session = Mock(get=Mock(return_value=access_token))
    return request_factory


class TestRequestsURL(TestCase):

    def setUp(self):
        self.request_factory = get_request_factory_with_session()

    @patch.object(tasks, 'requests', Mock(get=Mock()))
    def test_simply_requests_get(self):

        requests_url(self.request_factory, 'https://api.spotify.com/v1/me')
        tasks.requests.get.assert_called_once_with(
            'https://api.spotify.com/v1/me',
            headers={'Authorization': 'Bearer {}'.format('12345')}
        )


class TestCreateArtist(TestCase):

    def setUp(self):
        self.response = {
            'artists': [
                {
                    'id': '6ZLTlhejhndI4Rh53vYhrY',
                    'name': 'Ozzy Osbourne'
                }
            ]
        }

    def test_create_artist_from_response(self):

        # assure Artist table is empty
        self.assertFalse(Artist.objects.exists())

        # create Artist
        artist = get_or_create_artist(self.response)

        self.assertTrue(Artist.objects.exists())
        self.assertEqual(Artist.objects.first().id, artist.id)
        self.assertEqual(Artist.objects.first().name, artist.name)

    def test_not_create_same_artist_if_exists(self):

        # assure artist is in the table
        Artist.objects.create(
            **self.response['artists'][0]
        )
        self.assertEqual(Artist.objects.count(), 1)
        self.assertEqual(Artist.objects.first().id, self.response['artists'][0]['id'])

        # create Artist and check if exists
        get_or_create_artist(self.response)

        self.assertEqual(Artist.objects.count(), 1)


class TestCreateTrack(TestCase):

    def setUp(self):
        self.request_factory = get_request_factory_with_session()
        self.artist = {
            'id': '6ZLTlhejhndI4Rh53vYhrY',
            'name': 'Ozzy Osbourne'
        }
        self.track = {
            'id': '0LagWpYHMaQjbCeAIoOKVg',
            'name': 'Under the Graveyard'
        }
        self.response = {
            'artists': [
                {
                    'id': self.artist['id'],
                    'name': self.artist['name']
                }
            ],
            'name': self.track['name']
        }

    @responses.activate
    def test_create_track_for_existing_artist(self):

        responses.add(
            responses.GET,
            API_ENDPOINTS["track"] + self.track["id"],
            json=self.response,
            status=200
        )

        # create Artist
        artist = Artist.objects.create(**self.artist)
        self.assertTrue(Artist.objects.get(id=self.artist['id']))

        track = create_track(self.request_factory, self.track['id'])

        self.assertEqual(Track.objects.first(), track)
        self.assertEqual(Track.objects.first().id, self.track['id'])
        self.assertEqual(Track.objects.first().name, self.track['name'])
        self.assertEqual(Track.objects.first().artist.name, artist.name)

    @responses.activate
    def test_create_track_for_new_artist(self):

        responses.add(
            responses.GET,
            API_ENDPOINTS["track"] + self.track["id"],
            json=self.response,
            status=200
        )

        # assure Artist and Track tables are empty
        self.assertFalse(Artist.objects.exists())
        self.assertFalse(Track.objects.exists())

        track = create_track(self.request_factory, self.track['id'])

        self.assertEqual(Track.objects.first(), track)
        self.assertEqual(Track.objects.first().id, self.track['id'])
        self.assertEqual(Track.objects.first().name, self.track['name'])
        self.assertEqual(Artist.objects.first().id, self.artist['id'])
        self.assertEqual(Track.objects.first().artist.name, self.artist['name'])


class TestCreateAlbum(TestCase):

    def setUp(self):
        self.request_factory = get_request_factory_with_session()
        self.artist = {
            'id': '08GQAI4eElDnROBrJRGE0X',
            'name': 'Fleetwood Mac'
        }
        self.album = {
            'id': '1bt6q2SruMsBtcerNVtpZB',
            'name': 'Rumours'
        }
        self.response = {
            'artists': [
                {
                    'id': self.artist['id'],
                    'name': self.artist['name']
                }
            ],
            'id': self.album['id'],
            'name': self.album['name'],
            'images': [
                {},
                {
                    'url': 'https://dummy.url.com'
                }
            ]
        }

    @responses.activate
    def test_create_album_for_existing_artist(self):

        responses.add(
            responses.GET,
            API_ENDPOINTS["album"] + self.album["id"],
            json=self.response,
            status=200
        )

        # create Artist
        Artist.objects.create(**self.artist)
        self.assertTrue(Artist.objects.get(id=self.artist['id']))

        album, _ = create_album(self.request_factory, self.album['id'])

        self.assertEqual(Album.objects.first(), album)
        self.assertEqual(Album.objects.first().id, self.album['id'])
        self.assertEqual(Album.objects.first().name, self.album['name'])
        self.assertEqual(Album.objects.first().artist.name, self.artist['name'])

    @responses.activate
    def test_create_album_for_new_artist(self):

        responses.add(
            responses.GET,
            API_ENDPOINTS["album"] + self.album["id"],
            json=self.response,
            status=200
        )

        # assure Artist table is empty
        self.assertFalse(Artist.objects.exists())

        album, _ = create_album(self.request_factory, self.album['id'])

        self.assertEqual(Album.objects.first(), album)
        self.assertEqual(Album.objects.first().id, self.album['id'])
        self.assertEqual(Album.objects.first().name, self.album['name'])
        self.assertEqual(Album.objects.first().artist.name, self.artist['name'])
        self.assertEqual(Artist.objects.first().id, self.artist['id'])
        self.assertEqual(Artist.objects.first().name, self.artist['name'])


class TestCreateTrackFeatures(TestCase):

    def setUp(self):
        self.request_factory = get_request_factory_with_session()
        self.track = TrackFactory()
        self.response = {
            "danceability": random.random(),
            "speechiness": random.random(),
            "acousticness": random.random(),
            "valence": random.random(),
            "instrumentalness": random.random(),
            "energy": random.random(),
            "liveness": random.random()
        }

    @responses.activate
    def test_create_track_audio_features(self):

        responses.add(
            responses.GET,
            API_ENDPOINTS["track_audio_feature"] + self.track.id,
            json=self.response,
            status=200
        )

        track_features = create_track_audio_features(self.request_factory, self.track)

        self.assertTrue(TrackFeatures.objects.exists())
        self.assertTrue(Features.objects.exists())
        self.assertEqual(TrackFeatures.objects.first().track, self.track)
        self.assertEqual(TrackFeatures.objects.first().features, track_features)


class TestCreateTrackAndFeatures(TestCase):

    def setUp(self):
        self.request_factory = get_request_factory_with_session()
        self.track = TrackFactory()
        self.track_features = TrackFeaturesFactory(track=self.track)

    @patch.object(services, 'create_track_audio_features')
    @patch.object(services, 'create_track')
    def test_create_track_and_features(self, mock_create_track, mock_create_track_audio_features):
        mock_create_track.return_value = self.track
        mock_create_track_audio_features.return_value = self.track_features

        response = create_track_and_features(self.request_factory, self.track.id)

        mock_create_track.assert_called_once_with(
            self.request_factory,
            self.track.id
        )
        mock_create_track_audio_features.assert_called_once_with(
            self.request_factory,
            self.track
        )
        self.assertEqual(response, self.track)


class TestCreateAlbumFeatures(TestCase):

    def setUp(self):
        self.album = AlbumFactory()
        self.tracks = [
            TrackFactory()
            for _ in range(10)
        ]
        feature_value = Decimal(
            '{:.3f}'.format(random.randrange(0, 100) / 100)
        )
        self.features_values = dict(
            danceability=feature_value,
            speechiness=feature_value,
            acousticness=feature_value,
            valence=feature_value,
            instrumentalness=feature_value,
            energy=feature_value,
            liveness=feature_value
        )
        self.features = FeaturesFactory(**self.features_values)
        self.tracks_features = [
            TrackFeaturesFactory(track=track, features=self.features)
            for track in self.tracks
        ]

    def test_create_album_features(self):

        album_features = create_album_features(self.tracks, self.album)

        self.assertEqual(album_features.get_features, self.features_values)
        self.assertEqual(AlbumFeatures.objects.first().album, self.album)
        self.assertEqual(AlbumFeatures.objects.first().features.get_features, self.features_values)


class TestCreateTracksForAlbum(TestCase):

    def setUp(self):
        self.request = RequestFactory()
        self.tracks = [
            TrackFactory(id=str(id))
            for id in range(1, 6)
        ]
        self.album_data = {
            'tracks': {
                'items': []
            }
        }

    def test_get_tracks_already_in_db(self):

        self.album_data['tracks']['items'].extend([{'id': track.id} for track in self.tracks])

        tracks_list = create_tracks_from_album(self.request, self.album_data)

        self.assertEqual(tracks_list, self.tracks)

    @patch.object(services, 'create_track_and_features')
    def test_create_new_tracks(self, mock_create_track_and_features):

        self.album_data['tracks']['items'].extend([{'id': str(x) for x in range(6, 10)}])

        create_tracks_from_album(self.request, self.album_data)

        mock_create_track_and_features.assert_called()

    @patch.object(services, 'create_track_and_features')
    def test_get_tracks_and_create_new_tracks(self, mock_create_track_and_features):

        self.album_data['tracks']['items'].extend([{'id': track.id} for track in self.tracks])
        self.album_data['tracks']['items'].extend([{'id': '11'}])

        tracks_list = create_tracks_from_album(self.request, self.album_data)

        self.assertEqual(len(tracks_list), 6)
        self.assertEqual(tracks_list[:5], self.tracks)
        mock_create_track_and_features.assert_called_once_with(self.request, '11')


class TestCreateAlbumTracksAndFeatures(TestCase):

    def setUp(self):
        self.request = RequestFactory()

    @patch.object(services, 'create_album_features')
    @patch.object(services, 'create_tracks_from_album')
    @patch.object(services, 'create_album')
    def test_create_album_tracks_and_features(self,
                                              mock_create_album,
                                              mock_create_tracks_from_album,
                                              mock_create_album_features):

        album = AlbumFactory()
        album_data = {'dummy': 'data'}
        album_id = '123'
        mock_create_album.return_value = album, album_data
        tracks = [TrackFactory() for _ in range(5)]
        mock_create_tracks_from_album.return_value = tracks

        create_album_tracks_and_features(self.request, album_id)

        mock_create_album.assert_called_once_with(self.request, album_id)
        mock_create_tracks_from_album.assert_called_once_with(self.request, album_data)
        mock_create_album_features.called_once_with(tracks, album)
