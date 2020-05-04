from unittest.mock import patch

from django.urls import reverse
from django.test import TestCase

from spotify_app.models import Features
from spotify_app import api_endpoints
from spotify_app import selectors
from spotify_app import tasks
from .factories import (
    AlbumFactory,
    AlbumFeaturesFactory,
    ArtistFactory,
    SearchArtistFactory,
    TrackFactory,
    TrackFeaturesFactory,
)


def _add_access_token_to_client_session(client):
    session = client.session
    session['access_token'] = '12345'
    session.save()


class CallbackView(TestCase):

    def test_url_and_template(self):

        response = self.client.get(
            reverse('callback')
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'callback.html')

    def test_redirect_from_home_page_to_callback(self):

        response = self.client.get(
            reverse('index')
        )

        self.assertRedirects(response, '/callback/q')

    @patch.object(tasks, 'get_new_releases')
    @patch.object(api_endpoints, 'save_access_token_to_client_session')
    def test_redirect_from_callback_to_home_page(self,
                                                 get_new_releases_mock,
                                                 save_access_token_to_client_session_mock):

        _add_access_token_to_client_session(self.client)
        self.albums = [
            AlbumFactory()
            for _ in range(10)
        ]
        get_new_releases_mock.return_value = self.albums

        response = self.client.get(
            '{}{}'.format(reverse('callback'), '?code=ABCD123')
        )

        self.assertRedirects(response, '/')


class HomePageView(TestCase):

    def setUp(self):
        self.albums = [
            AlbumFactory()
            for _ in range(10)
        ]
        _add_access_token_to_client_session(self.client)

    @patch.object(tasks, 'get_new_releases')
    def test_url_and_template(self, get_new_releases_mock):

        get_new_releases_mock.return_value = self.albums
        response = self.client.get(
            reverse('index')
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    @patch.object(tasks, 'get_new_releases')
    def test_all_albums_in_html(self, get_new_releases_mock):

        get_new_releases_mock.return_value = self.albums
        response = self.client.get(
            reverse('index')
        )

        for album in self.albums:
            self.assertContains(response, album.name)

    @patch('spotify_app.views.get_new_releases')
    def test_urls_for_all_albums_in_html(self, get_new_releases_mock):

        get_new_releases_mock.return_value = self.albums
        response = self.client.get(
            reverse('index')
        )

        for album in self.albums:
            album_url = reverse('album', args=[album.id])
            self.assertContains(response, album_url)


class UserRecentlyPlayedView(TestCase):

    def setUp(self):
        self.tracks = [
            TrackFactory()
            for _ in range(20)
        ]
        _add_access_token_to_client_session(self.client)

    @patch('spotify_app.views.get_user_recently_played')
    def test_url_and_template(self, mock_func):
        mock_func.return_value = self.tracks
        response = self.client.get(
            reverse('recently_played')
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recently_played.html')

    @patch('spotify_app.views.get_user_recently_played')
    def test_all_tracks_in_html(self, mock_func):
        mock_func.return_value = self.tracks
        response = self.client.get(
            reverse('recently_played')
        )

        for track in self.tracks:
            self.assertContains(response, track.name)

    @patch('spotify_app.views.get_user_recently_played')
    def test_urls_for_all_tracks_in_html(self, mock_func):
        mock_func.return_value = self.tracks
        response = self.client.get(
            reverse('recently_played')
        )

        for track in self.tracks:
            track_url = reverse('track', args=[track.id])
            self.assertContains(response, track_url)


class TrackTableView(TestCase):

    def setUp(self):
        self.tracks_and_features = [
            TrackFeaturesFactory()
            for _ in range(10)
        ]
        self.tracks = [
            x.track
            for x in self.tracks_and_features
        ]
        self.features = [
            x.features
            for x in self.tracks_and_features
        ]

        _add_access_token_to_client_session(self.client)

    def test_url_and_template(self):
        response = self.client.get(
            reverse('tracks_table')
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracks_table.html')

    def test_all_track_names_in_html(self):
        response = self.client.get(
            reverse('tracks_table')
        )

        for track in self.tracks:
            self.assertContains(response, track.name)

    def test_all_artist_names_in_html(self):
        response = self.client.get(
            reverse('tracks_table')
        )

        for track in self.tracks:
            self.assertContains(response, track.artist.name)

    def test_all_features_in_html(self):
        features_names = Features().get_fields_names

        response = self.client.get(
            reverse('tracks_table')
        )

        for feat_name in features_names:
            self.assertContains(response, feat_name.capitalize())

    def test_all_features_values_in_html(self):
        features_names = Features().get_fields_names

        response = self.client.get(
            reverse('tracks_table')
        )

        for feature in self.features:
            for feat_name in features_names:
                x_feat = getattr(feature, feat_name)
                self.assertContains(response, x_feat)


class AlbumTableView(TestCase):

    def setUp(self):
        self.albums_and_features = [
            AlbumFeaturesFactory()
            for _ in range(10)
        ]
        self.albums = [
            x.album
            for x in self.albums_and_features
        ]
        self.features = [
            x.features
            for x in self.albums_and_features
        ]

        _add_access_token_to_client_session(self.client)

    def test_url_and_template(self):
        response = self.client.get(
            reverse('albums_table')
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'albums_table.html')

    def test_all_album_names_in_html(self):
        response = self.client.get(
            reverse('albums_table')
        )

        for album in self.albums:
            self.assertContains(response, album.name)

    def test_all_artist_names_in_html(self):
        response = self.client.get(
            reverse('albums_table')
        )

        for album in self.albums:
            self.assertContains(response, album.artist.name)

    def test_all_features_in_html(self):
        features_names = Features().get_fields_names

        response = self.client.get(
            reverse('albums_table')
        )

        for feat_name in features_names:
            self.assertContains(response, feat_name.capitalize())

    def test_all_features_values_in_html(self):
        features_names = Features().get_fields_names

        response = self.client.get(
            reverse('albums_table')
        )

        for feature in self.features:
            for feat_name in features_names:
                x_feat = getattr(feature, feat_name)
                self.assertContains(response, x_feat)


class TrackDetailView(TestCase):

    def setUp(self):
        self.track_and_features = TrackFeaturesFactory()
        self.track = self.track_and_features.track
        self.features = self.track_and_features.features

        _add_access_token_to_client_session(self.client)

    def test_url_and_template(self):
        response = self.client.get(
            reverse('track', args=[self.track.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'track.html')

    def test_track_name_in_html(self):
        response = self.client.get(
            reverse('track', args=[self.track.id])
        )

        self.assertContains(response, self.track.name)

    def test_artist_name_in_html(self):
        response = self.client.get(
            reverse('track', args=[self.track.id])
        )

        self.assertContains(response, self.track.artist.name)

    def test_all_features_in_html(self):
        features_names = Features().get_fields_names

        response = self.client.get(
            reverse('track', args=[self.track.id])
        )

        for feat_name in features_names:
            self.assertContains(response, feat_name.capitalize())

    def test_all_features_values_in_html(self):
        features_names = Features().get_fields_names

        response = self.client.get(
            reverse('track', args=[self.track.id])
        )

        for feat_name in features_names:
            x_feat = getattr(self.features, feat_name)
            self.assertContains(response, x_feat)

    def test_all_features_values_for_chart_in_html(self):
        features_values = self.features.get_features_for_chart()

        response = self.client.get(
            reverse('track', args=[self.track.id])
        )

        for numb in features_values:
            self.assertContains(response, numb)

    @patch.object(selectors, 'create_track_and_features')
    def test_create_track_when_does_not_exist(self, create_track_and_features_mock):
        track_id = 'x233Ffs34kskzz'

        self.client.get(
            reverse('track', args=[track_id])
        )

        track = TrackFactory(id=track_id)
        track_and_features = TrackFeaturesFactory(track=track)
        create_track_and_features_mock.return_value = track_and_features

        create_track_and_features_mock.assert_called_once()

        response = self.client.get(
            reverse('track', args=[track_id])
        )
        self.assertContains(response, track.name)


class AlbumDetailView(TestCase):

    def setUp(self):
        self.tracks = [TrackFactory() for _ in range(13)]
        self.album = AlbumFactory.create(tracks=self.tracks)
        self.album_and_features = AlbumFeaturesFactory.create(album=self.album)
        self.features = self.album_and_features.features

        _add_access_token_to_client_session(self.client)

    def test_url_and_template(self):
        response = self.client.get(
            reverse('album', args=[self.album.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'album.html')

    def test_album_name_in_html(self):
        response = self.client.get(
            reverse('album', args=[self.album.id])
        )

        self.assertContains(response, self.album.name)

    def test_album_image_in_html(self):
        response = self.client.get(
            reverse('album', args=[self.album.id])
        )

        self.assertContains(response, self.album.image)

    def test_artist_name_in_html(self):
        response = self.client.get(
            reverse('album', args=[self.album.id])
        )

        self.assertContains(response, self.album.artist.name)

    def test_all_tracks_in_html(self):
        response = self.client.get(
            reverse('album', args=[self.album.id])
        )

        for track in self.tracks:
            self.assertContains(response, track.name)

    def test_urls_for_all_tracks_in_html(self):
        response = self.client.get(
            reverse('album', args=[self.album.id])
        )

        for track in self.tracks:
            track_url = reverse('track', args=[track.id])
            self.assertContains(response, track_url)

    def test_all_features_in_html(self):
        features_names = Features().get_fields_names

        response = self.client.get(
            reverse('album', args=[self.album.id])
        )

        for feat_name in features_names:
            self.assertContains(response, feat_name.capitalize())

    def test_all_features_values_in_html(self):
        features_names = Features().get_fields_names

        response = self.client.get(
            reverse('album', args=[self.album.id])
        )

        for feature in features_names:
            x_feature = getattr(self.features, feature)
            self.assertContains(response, x_feature)

    def test_all_features_values_for_chart_in_html(self):
        features_values = self.features.get_features_for_chart()

        response = self.client.get(
            reverse('album', args=[self.album.id])
        )

        for feature_value in features_values:
            self.assertContains(response, feature_value)

    @patch.object(selectors, 'create_album_tracks_and_features')
    def test_create_album_when_does_not_exist(self, create_album_tracks_and_features_mock):
        album_id = '123hkaCXX123kk'

        self.client.get(
            reverse('album', args=[album_id])
        )

        album = AlbumFactory(id=album_id)
        album_and_features = AlbumFeaturesFactory(album=album)
        create_album_tracks_and_features_mock.return_value = album_and_features

        create_album_tracks_and_features_mock.assert_called_once()

        response = self.client.get(
            reverse('album', args=[album_id])
        )
        self.assertContains(response, album.name)


class ArtistDetailView(TestCase):

    def setUp(self):
        self.artist = ArtistFactory()
        self.albums = [
            AlbumFactory(artist=self.artist)
            for _ in range(6)
        ]

        _add_access_token_to_client_session(self.client)

    @patch('spotify_app.views.get_artist_and_albums')
    def test_url_and_template(self, mock_artist_albums):
        mock_artist_albums.return_value = self.artist.name, self.albums
        response = self.client.get(
            reverse('artist', args=[self.artist.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'artist.html')

    @patch('spotify_app.views.get_artist_and_albums')
    def test_artist_in_html(self, mock_artist_albums):
        mock_artist_albums.return_value = self.artist.name, self.albums
        response = self.client.get(
            reverse('artist', args=[self.artist.id])
        )

        self.assertContains(response, self.artist.name)

    @patch('spotify_app.views.get_artist_and_albums')
    def test_all_albums_in_html(self, mock_artist_albums):
        mock_artist_albums.return_value = self.artist.name, self.albums
        response = self.client.get(
            reverse('artist', args=[self.artist.id])
        )

        for album in self.albums:
            self.assertContains(response, album.name)

    @patch('spotify_app.views.get_artist_and_albums')
    def test_urls_for_all_albums_in_html(self, mock_artist_albums):
        mock_artist_albums.return_value = self.artist.name, self.albums
        response = self.client.get(
            reverse('artist', args=[self.artist.id])
        )

        for album in self.albums:
            album_url = reverse('album', args=[album.id])
            self.assertContains(response, album_url)


class SearchView(TestCase):

    def setUp(self):
        self.searching_artist = 'found'
        self.found_artists = [
            SearchArtistFactory()
            for _ in range(5)
        ]
        _add_access_token_to_client_session(self.client)

    @patch('spotify_app.views.get_search_results')
    def test_url_and_template(self, mock_search_results):
        mock_search_results.return_value = self.found_artists, '5'

        response = self.client.get(
            '{}{}'.format(reverse('search'), f'?q={self.searching_artist}')
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')

    @patch('spotify_app.views.get_search_results')
    def test_found_searching_artist(self, mock_search_results):
        mock_search_results.return_value = self.found_artists, '5'

        response = self.client.get(
            '{}{}'.format(reverse('search'), f'?q={self.searching_artist}')
        )
        self.assertContains(response, self.searching_artist)
        self.assertContains(response, '5')
        for artist in self.found_artists:
            self.assertContains(response, artist.name)

    @patch('spotify_app.views.get_search_results')
    def test_ulrs_for_found_searching_artist(self, mock_search_results):
        mock_search_results.return_value = self.found_artists, '5'

        response = self.client.get(
            '{}{}'.format(reverse('search'), f'?q={self.searching_artist}')
        )
        for artist in self.found_artists:
            artist_url = reverse('artist', args=[artist.id])
            self.assertContains(response, artist_url)

    @patch('spotify_app.views.get_search_results')
    def test_not_found_searching_artist(self, mock_search_results):
        mock_search_results.return_value = [], '0'
        searching_artist = f'not_{self.searching_artist}'

        response = self.client.get(
            '{}{}'.format(reverse('search'), f'?q={searching_artist}')
        )
        self.assertContains(response, searching_artist)
        self.assertContains(response, '0')
