from django.urls import path, re_path

from spotify_app import views


urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path(
        "recently_played/",
        views.UserRecentlyPlayedView.as_view(),
        name="recently_played",
    ),
    # TODO: fix track url, leave only id and change it to slug
    re_path(
        "^track/(?P<track_id>[a-zA-Z0-9]+)/$",
        views.TrackDetailView.as_view(),
        name="track",
    ),
    path("tracks_table/", views.TracksTableView.as_view(), name="tracks_table"),
    path("album/<slug:album_id>/", views.AlbumDetailView.as_view(), name="album"),
    path("albums_table/", views.AlbumTableView.as_view(), name="albums_table"),
    path("artist/<slug:artist_id>/", views.ArtistDetailView.as_view(), name="artist"),
    path(
        "spotify_playlists/",
        views.SpotifyPlaylistsView.as_view(),
        name="spotify_playlists",
    ),
    path(
        "playlist/<slug:playlist_id>/",
        views.PlaylistDetailView.as_view(),
        name="playlist",
    ),
    path("search/", views.SearchView.as_view(), name="search"),
]
