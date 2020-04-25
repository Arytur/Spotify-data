from unittest.mock import patch, MagicMock

from django.test import RequestFactory, TestCase
from django.urls import reverse

from spotify_app import api_endpoints
from spotify_app.api_endpoints import save_access_token_to_client_session, SPOTIFY_TOKEN_URL

import responses


class TestSessionAccessToken(TestCase):

    def setUp(self):
        self.response = {
            "access_token": 888,
            "refresh_token": 999,
            "expires_in": 360
        }

    @responses.activate
    def test_saving_access_token_into_session(self):

        responses.add(
            responses.POST,
            SPOTIFY_TOKEN_URL,
            json=self.response,
            status=200
        )

        self.client.get(
            '{}{}'.format(reverse('callback'), '?code=ABCD123')
        )
        session = self.client.session

        self.assertEqual(session["access_token"], self.response["access_token"])
        self.assertEqual(session["refresh_token"], self.response["refresh_token"])
