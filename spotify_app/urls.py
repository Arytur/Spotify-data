from django.urls import path, re_path

from spotify_app import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('recently_played/', views.UserRecentlyPlayedView.as_view(), name='recently_played'),
    path('album/<slug:album_id>/', views.AlbumView.as_view(), name='album'),
    path('spotify_playlists/', views.SpotifyPlaylistsView.as_view(), name='spotify_playlists'),
    path('playlist/<slug:playlist_id>/', views.PlaylistView.as_view(), name='playlist'),
    # TODO: fix track url, leave only id and change it to slug
    re_path('^track/(?P<track_id>[a-zA-Z0-9]+)/(?P<track_artist>.*)/(?P<track_name>.*)/$',
        views.TrackAudioFeaturesView.as_view(), name='track'),
    path('tracks_table/', views.TracksTableView.as_view(), name='tracks_table'),
    path('albums_table/', views.AlbumTableView.as_view(), name='albums_table'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('artist/<slug:artist_id>/', views.ArtistView.as_view(), name='artist'),
]
