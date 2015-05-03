"""
URLS specific to the leaderboard app. User authentication URL's should be in main urls.py.
"""
from django.conf.urls import url
from views import GoogleCallBack, GameListView, UserProfileView, UserGameProfileView

urlpatterns = [
    url(r'^googleCallBack/(?P<key>[.*]+)/$', GoogleCallBack.as_view()),
    url(r'^game-list/$', GameListView.as_view()),
    url(r'^user-profile/$', UserProfileView.as_view()),
    url(r'^user-game-profile/$', UserGameProfileView.as_view()),
]
