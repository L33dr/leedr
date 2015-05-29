"""
URLS specific to the leaderboard app. User authentication URL's should be in main urls.py.
"""
from django.conf.urls import url
from views import GoogleCallBack, GameListView, UserProfileView, UserGameProfileView, Comment, UserProfileUpdateView, \
    UserGameProfileDeleteView

urlpatterns = [
    url(r'^googleCallBack/(?P<key>[.*]+)/$', GoogleCallBack.as_view()),
    url(r'^game-list/$', GameListView.as_view(), name="game-list"),
    url(r'^user-profile/$', UserProfileView.as_view(), name="profile"),
    url(r'^user-profile/update/$', UserProfileUpdateView.as_view(), name="update-profile"),
    url(r'^user-game-profile/$', UserGameProfileView.as_view(), name="game-profile"),
    url(r'^user-game-profile/delete/(?P<game>[A-Za-z0-9_.]+)/$', UserGameProfileDeleteView.as_view(), name="delete-game-profile"),
    url(r'^comment/$', Comment.as_view(), name="post-comment"),
]
