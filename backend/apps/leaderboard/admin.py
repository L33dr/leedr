from django.contrib import admin
from models import GameDetail
from models import UserProfile
from models import UserGameProfile
from game_models.lol_game_model import LOLGameData
from game_models.lol_game_model import LOLPlayerStatSummary
from game_models.lol_game_model import LOLAggregatedStats

admin.site.register(GameDetail)
admin.site.register(UserProfile)
admin.site.register(UserGameProfile)
admin.site.register(LOLGameData)
admin.site.register(LOLPlayerStatSummary)
admin.site.register(LOLAggregatedStats)