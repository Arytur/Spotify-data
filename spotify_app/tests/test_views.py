import json
from unittest.mock import patch

from django.test import TestCase

from .factories import (
    AlbumFactory,
    AlbumFeaturesFactory,
    TrackFactory,
    TrackFeaturesFactory,
)


def _add_access_token_to_client_session(client):
    session = client.session
    session['access_token'] = '12345'
    session.save()


class TestUrlsAndTemplatesUsed(TestCase):

    def test_callback_page(self):
        response = self.client.get('/callback/q')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'callback.html')

    def test_redirect_from_home_page_to_callback(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/callback/q')

    @patch('spotify_app.tasks.requests_url')
    def test_home_page(self, mock_func):
        json_file = open('spotify_app/tests/fixtures/new_releases_raw.json')
        resp_file = json.load(json_file)
        mock_func.return_value = resp_file
        _add_access_token_to_client_session(self.client)
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    @patch('spotify_app.tasks.requests_url')
    def test_recently_played_page(self, mock_func):
        _add_access_token_to_client_session(self.client)
        response = self.client.get('/recently_played/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recently_played.html')

    @patch('spotify_app.tasks.requests_url')
    def test_tracks_table_page(self, mock_func):
        _add_access_token_to_client_session(self.client)
        response = self.client.get('/tracks_table/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracks_table.html')

    @patch('spotify_app.tasks.requests_url')
    def test_albums_table_page(self, mock_func):
        _add_access_token_to_client_session(self.client)
        response = self.client.get('/albums_table/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'albums_table.html')


class TrackDetailView(TestCase):

    def setUp(self):
        self.track_and_features = TrackFeaturesFactory()
        self.track = self.track_and_features.track
        self.features = self.track_and_features.features

        _add_access_token_to_client_session(self.client)

    def test_url_and_template(self):
        response = self.client.get(
            f'/track/{self.track.id}/'
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'track.html')

    def test_track_name_in_html(self):
        response = self.client.get(
            f'/track/{self.track.id}/'
        )
        self.assertContains(response, self.track.name)

    def test_artist_name_in_html(self):
        response = self.client.get(
            f'/track/{self.track.id}/'
        )
        self.assertContains(response, self.track.artist.name)

    def test_all_features_in_html(self):
        features_names = self.features.get_fields_names

        response = self.client.get(
            f'/track/{self.track.id}/'
        )

        for feat_name in features_names:
            self.assertContains(response, feat_name.capitalize())

    def test_all_features_values_in_html(self):
        features_names = self.features.get_fields_names

        response = self.client.get(
            f'/track/{self.track.id}/'
        )

        for feat_name in features_names:
            x_feat = getattr(self.features, feat_name)
            self.assertContains(response, x_feat)

    def test_all_features_values_for_chart_in_html(self):
        features_values = self.features.get_features_for_chart()

        response = self.client.get(
            f'/track/{self.track.id}/'
        )

        for numb in features_values:
            self.assertContains(response, numb)


class AlbumDetailView(TestCase):

    def setUp(self):
        self.album_and_features = AlbumFeaturesFactory()
        self.album = self.album_and_features.album
        self.features = self.album_and_features.features

        _add_access_token_to_client_session(self.client)

    def test_url_and_template(self):
        response = self.client.get(
            f'/album/{self.album.id}/'
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'album.html')

    def test_album_name_in_html(self):
        response = self.client.get(
            f'/album/{self.album.id}/'
        )
        self.assertContains(response, self.album.name)

    def test_artist_name_in_html(self):
        response = self.client.get(
            f'/album/{self.album.id}/'
        )
        self.assertContains(response, self.album.artist.name)

    def test_all_tracks_in_html(self):
        tracks = [TrackFactory() for _ in range(13)]
        album = AlbumFactory.create(tracks=tracks)
        AlbumFeaturesFactory.create(
           album=album
        )

        response = self.client.get(
            f'/album/{album.id}/'
        )

        for track in tracks:
            self.assertContains(response, track.name)

    def test_all_features_in_html(self):
        features_names = self.features.get_fields_names

        response = self.client.get(
            f'/album/{self.album.id}/'
        )

        for feat_name in features_names:
            self.assertContains(response, feat_name.capitalize())

    # def test_all_features_values_in_html(self):
    #     features_names = self.features.get_fields_names

    #     response = self.client.get(
    #         f'/album/{self.album.id}/'
    #     )

    #     for feat_name in features_names:
    #         x_feat = getattr(self.features, feat_name)
    #         self.assertContains(response, x_feat)

    def test_all_features_values_for_chart_in_html(self):
        features_values = self.features.get_features_for_chart()

        response = self.client.get(
            f'/album/{self.album.id}/'
        )

        for numb in features_values:
            self.assertContains(response, numb)
