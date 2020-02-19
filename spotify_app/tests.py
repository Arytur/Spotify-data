import json

from django.test import TestCase
from unittest.mock import patch


class TestUrlsAndTemplatesUsed(TestCase):

    def _add_access_token_to_client_session(self):
        session = self.client.session
        session['access_token'] = '12345'
        session.save()

    def test_callback_page(self):
        response = self.client.get('/callback/q')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'callback.html')

    def test_redirect_from_home_page_to_callback(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/callback/q')

    @patch('spotify_app.tasks.requests_url')
    def test_home_page(self, mock_func):
        json_file = open('tests/fixtures/new_releases_raw.json')
        resp_file = json.load(json_file)
        mock_func.return_value = resp_file
        self._add_access_token_to_client_session()
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    @patch('spotify_app.tasks.requests_url')
    def test_recently_played_page(self, mock_func):
        self._add_access_token_to_client_session()
        response = self.client.get('/recently_played/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recently_played.html')

    @patch('spotify_app.tasks.requests_url')
    def test_tracks_table_page(self, mock_func):
        self._add_access_token_to_client_session()
        response = self.client.get('/tracks_table/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracks_table.html')

    @patch('spotify_app.tasks.requests_url')
    def test_albums_table_page(self, mock_func):
        self._add_access_token_to_client_session()
        response = self.client.get('/albums_table/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'albums_table.html')
