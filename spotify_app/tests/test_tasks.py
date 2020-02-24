import json

from django.http import HttpRequest
from django.test import TestCase
from unittest.mock import patch

from spotify_app.models import (
    Album,
    Artist,
    Features,
    Track,
    TrackFeatures
    )
from spotify_app.tasks import (
    create_album,
    create_artist,
    create_track,
    create_track_audio_features,
)


class TestArtistCreate(TestCase):
    response = {
        'artists': [
            {
                'id': '6ZLTlhejhndI4Rh53vYhrY',
                'name': 'Ozzy Osbourne'
            }
        ]
    }

    def test_create_artist_from_response(self):

        # check if Artist table is empty
        self.assertFalse(Artist.objects.exists())

        # create Artist and check if exists
        create_artist(self.response)
        self.assertTrue(Artist.objects.exists())

    def test_not_create_same_artist_from_response(self):

        # check if Artist is in the table
        Artist.objects.create(
            id='6ZLTlhejhndI4Rh53vYhrY',
            name='Ozzy Osbourne'
        )
        self.assertEqual(Artist.objects.count(), 1)

        # create Artist and check if exists
        create_artist(self.response)
        self.assertEqual(Artist.objects.count(), 1)


class TestTrackCreate(TestCase):
    artist = dict(
        id='6ZLTlhejhndI4Rh53vYhrY',
        name='Ozzy Osbourne'
    )
    track = dict(
        id='0LagWpYHMaQjbCeAIoOKVg',
        name='Under the Graveyard'
    )

    @patch('spotify_app.tasks.requests_url')
    def test_create_track_for_existing_artist(self, mock_func):
        json_file = open('spotify_app/tests/fixtures/track_response_raw.json')
        mock_func.return_value = json.load(json_file)
        # TODO: Use Request Factory
        request = HttpRequest()

        # create Artist and check if exists
        Artist.objects.create(**self.artist)
        self.assertTrue(Artist.objects.get(id=self.artist['id']))

        track = create_track(request, self.track['id'])
        self.assertEqual(Track.objects.first(), track)
        self.assertEqual(Track.objects.first().id, self.track['id'])
        self.assertEqual(Track.objects.first().name, self.track['name'])

    @patch('spotify_app.tasks.requests_url')
    def test_create_track_for_new_artist(self, mock_func):
        json_file = open('spotify_app/tests/fixtures/track_response_raw.json')
        mock_func.return_value = json.load(json_file)
        # TODO: Use Request Factory
        request = HttpRequest()

        # check if Artist table is empty
        self.assertFalse(Artist.objects.exists())

        track = create_track(request, self.track['id'])
        self.assertEqual(Track.objects.first(), track)
        self.assertEqual(Track.objects.first().id, self.track['id'])
        self.assertEqual(Track.objects.first().name, self.track['name'])
        self.assertEqual(Artist.objects.first().id, self.artist['id'])


class TestAlbumCreate(TestCase):
    artist = dict(
        id='08GQAI4eElDnROBrJRGE0X',
        name='Fleetwood Mac'
    )
    album = dict(
        id='1bt6q2SruMsBtcerNVtpZB',
        name='Rumours'
    )

    @patch('spotify_app.tasks.requests_url')
    def test_create_album_for_existing_artist(self, mock_func):
        json_file = open('spotify_app/tests/fixtures/album_response_raw.json')
        mock_func.return_value = json.load(json_file)
        # TODO: Use Request Factory
        request = HttpRequest()

        # create Artist and check if exists
        Artist.objects.create(**self.artist)
        self.assertTrue(Artist.objects.get(id=self.artist['id']))

        album, _ = create_album(request, self.album['id'])
        self.assertEqual(Album.objects.first(), album)
        self.assertEqual(Album.objects.first().id, self.album['id'])
        self.assertEqual(Album.objects.first().name, self.album['name'])

    @patch('spotify_app.tasks.requests_url')
    def test_create_album_for_new_artist(self, mock_func):
        json_file = open('spotify_app/tests/fixtures/album_response_raw.json')
        mock_func.return_value = json.load(json_file)
        # TODO: Use Request Factory
        request = HttpRequest()

        # check if Artist table is empty
        self.assertFalse(Artist.objects.exists())

        album, _ = create_album(request, self.album['id'])
        self.assertEqual(Album.objects.first(), album)
        self.assertEqual(Album.objects.first().id, self.album['id'])
        self.assertEqual(Album.objects.first().name, self.album['name'])
        self.assertEqual(Artist.objects.first().id, self.artist['id'])


class TestFeaturesCreate(TestCase):
    artist = dict(
        id='6ZLTlhejhndI4Rh53vYhrY',
        name='Ozzy Osbourne'
    )

    @patch('spotify_app.tasks.requests_url')
    def test_create_track_audio_features(self, mock_func):
        json_file = open('spotify_app/tests/fixtures/audio_features_raw.json')
        mock_func.return_value = json.load(json_file)

        # TODO: Use Request Factory
        request = HttpRequest()

        artist = Artist.objects.create(**self.artist)
        track = Track.objects.create(
            id='12345',
            name='test track',
            artist=artist
        )
        track_features = create_track_audio_features(request, track)
        self.assertTrue(TrackFeatures.objects.exists())
        self.assertTrue(Features.objects.exists())
        self.assertEqual(TrackFeatures.objects.first().track, track)
        self.assertEqual(TrackFeatures.objects.first().features, track_features)

    # TODO: album audio features
