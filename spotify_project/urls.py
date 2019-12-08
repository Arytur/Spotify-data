"""spotify_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path

from spotify_app.views import (
    Index,
    Callback,
    UserRecentlyPlayedView,
    AlbumView,
    SpotifyPlaylistsView,
    PlaylistView,
    TrackAudioFeaturesView,
    TracksTableView,
    AlbumTableView,
    SearchView,
    ArtistView
) 

# TODO: include for the app urls
# TODO: fix track url, leave only id and change it to slug

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index'),
    path('callback/q', Callback.as_view(), name='callback'),
    path('recently_played/', UserRecentlyPlayedView.as_view(), name='recently_played'),
    path('album/<slug:album_id>/', AlbumView.as_view(), name='album'),
    path('spotify_playlists/', SpotifyPlaylistsView.as_view(), name='spotify_playlists'),
    path('playlist/<slug:playlist_id>/', PlaylistView.as_view(), name='playlist'),
    re_path('^track/(?P<track_id>[a-zA-Z0-9]+)/(?P<track_artist>.*)/(?P<track_name>.*)/$',
        TrackAudioFeaturesView.as_view(), name='track'),
    path('tracks_table/', TracksTableView.as_view(), name='tracks_table'),
    path('albums_table/', AlbumTableView.as_view(), name='albums_table'),
    path('search/', SearchView.as_view(), name='search'),
    path('artist/<slug:artist_id>/', ArtistView.as_view(), name='artist')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
