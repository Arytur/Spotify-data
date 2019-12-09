from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from spotify_app.views import Callback

urlpatterns = [
    path('admin/', admin.site.urls),
    path('callback/q', Callback.as_view(), name='callback'),
    path('', include('spotify_app.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
