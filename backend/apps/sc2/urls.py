"""
URLS specific to the leaderboard app. User authentication URL's should be in main urls.py.
"""
from django.conf.urls import url
from apps.sc2.views import SC2GameDataView

urlpatterns = [
    url(r'^user-data/$', SC2GameDataView.as_view()),
]
