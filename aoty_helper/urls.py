from django.contrib import admin
from django.urls import path
from album_app import views as album_views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import re_path, include
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', album_views.index, name='indexView'),
    path(r'(?P<str:year_param>\w+)\$', album_views.index, name="indexView"),
    path('add_album', album_views.createView_album, name='createView_album'),
    path('settings', album_views.settingsView, name="settingsView"),
    path('feedback', album_views.feedbackView, name="feedbackView"),

    path('get_new/spotify/', album_views.getNewFromSpotifyView, name="newFromSpotifyView"),

    path('callback/', album_views.callbackView, name="callback"),
    path('refresh_token/', album_views.refreshTokenView, name="refresh_token"),

    path('details=<uuid:ultID>', album_views.detailView, name="detailView"),
    path('details=<uuid:ultID>/edit', album_views.editView, name="editView"),
    path('details=<uuid:ultID>/delete', album_views.deleteView, name="deleteView"),

    # User Authentiation/Registration
    path("accounts/", include("accounts.urls")),
    path('accounts/', include("django.contrib.auth.urls")),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
        }),
    ]

handler404 = 'album_app.views.view_404'
handler500 = 'album_app.views.view_500'
