from django.conf.urls import include, url
from django.contrib import admin
from backend.apps.leaderboard.views import FacebookLogin, GoogleLogin, TwitchLogin
urlpatterns = [
    # Examples:
    # url(r'^$', 'leaderboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view()),
    url(r'^rest-auth/google/$', GoogleLogin.as_view()),
    url(r'^rest-auth/twitch/$', TwitchLogin.as_view())
]
