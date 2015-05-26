"""
URLS specific to the leaderboard app. User authentication URL's should be in main urls.py.
"""
from django.conf.urls import url
from apps.lol.views import LOLAllStats

urlpatterns = [
    url(r'^user-data/$', LOLAllStats.as_view()),
]
