from django.contrib import admin
from apps.lol.models import LOLGameData, LOLAggregatedStats, LOLPlayerStatSummary
admin.site.register(LOLGameData)
admin.site.register(LOLPlayerStatSummary)
admin.site.register(LOLAggregatedStats)