"""
URLS specific to the leaderboard app. User authentication URL's should be in main urls.py.
"""
from django.conf.urls import url
from views import GoogleCallBack

urlpatterns = [
    url(r'^googleCallBack/(?P<key>[.*]+)/$', GoogleCallBack.as_view()),
]
