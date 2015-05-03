"""
URLS specific to the leaderboard app. User authentication URL's should be in main urls.py.
"""
from django.conf.urls import url
from views import GoogleCallBack, GameListView, UserProfileView, UserGameProfileView

urlpatterns = [
    url(r'^googleCallBack/(?P<key>[.*]+)/$', GoogleCallBack.as_view()),
    url(r'^gameList/$', GameListView.as_view(), name='game_list'),
    url(r'^userProfile/$', UserProfileView.as_view(), name='user_profile'),
    url(r'^userGameProfile/$', UserGameProfileView.as_view(), name='user_game_profile'),
]
