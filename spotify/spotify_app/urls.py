from django.urls import path

from spotify_app import views


# TODO: search/callback q?

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path(
        "recently_played/",
        views.UserRecentlyPlayedView.as_view(),
        name="recently_played",
    ),
    path(
        "track/<slug:track_id>/",
        views.TrackDetailView.as_view(),
        name="track",
    ),
    path("tracks_table/", views.TracksTableView.as_view(), name="tracks_table"),
    path("album/<slug:album_id>/", views.AlbumDetailView.as_view(), name="album"),
    path("albums_table/", views.AlbumTableView.as_view(), name="albums_table"),
    path("artist/<slug:artist_id>/", views.ArtistDetailView.as_view(), name="artist"),
    path("search/", views.SearchView.as_view(), name="search"),
]
