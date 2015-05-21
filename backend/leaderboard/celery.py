from __future__ import absolute_import

from celery import Celery
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leaderboard.settings')

from django.conf import settings
app = Celery('leaderboard')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print 'Request: {0!r}'.format(self.request)

