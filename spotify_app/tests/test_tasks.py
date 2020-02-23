import json

from django.http import HttpRequest
from django.test import TestCase
from unittest.mock import patch

from spotify_app.models import Album, Artist, Track
from spotify_app.tasks import create_track, create_album


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
        request = HttpRequest()

        # check if Artist table is empty
        self.assertFalse(Artist.objects.exists())

        album, _ = create_album(request, self.album['id'])
        self.assertEqual(Album.objects.first(), album)
        self.assertEqual(Album.objects.first().id, self.album['id'])
        self.assertEqual(Album.objects.first().name, self.album['name'])
        self.assertEqual(Artist.objects.first().id, self.artist['id'])
