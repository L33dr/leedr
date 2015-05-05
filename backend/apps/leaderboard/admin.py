from django.contrib import admin
from models import GameDetail
from models import UserProfile
from models import UserGameProfile
from game_models.lol_game_model import LOLGameData
from game_models.lol_game_model import LOLPlayerStatSummary
from game_models.lol_game_model import LOLAggregatedStats
from apps.leaderboard.game_models.sc2_game_model import SC2Career
from apps.leaderboard.game_models.sc2_game_model import Terran
from apps.leaderboard.game_models.sc2_game_model import Zerg
from apps.leaderboard.game_models.sc2_game_model import Protoss
from apps.leaderboard.game_models.sc2_game_model import SwarmLevels
from apps.leaderboard.game_models.sc2_game_model import Campaign
from apps.leaderboard.game_models.sc2_game_model import Season
from apps.leaderboard.game_models.sc2_game_model import RewardsList
from apps.leaderboard.game_models.sc2_game_model import UserCategoryPoints
from apps.leaderboard.game_models.sc2_game_model import UserAchievementPoints
from apps.leaderboard.game_models.sc2_game_model import UserAchievement
from apps.leaderboard.game_models.sc2_game_model import UserAchievementList
from apps.leaderboard.game_models.sc2_game_model import SC2GameData
from apps.leaderboard.game_models.sc2_game_model import Achievement
from apps.leaderboard.game_models.sc2_game_model import Category
from apps.leaderboard.game_models.sc2_game_model import ChildCategory

admin.site.register(GameDetail)
admin.site.register(UserProfile)
admin.site.register(UserGameProfile)
admin.site.register(LOLGameData)
admin.site.register(LOLPlayerStatSummary)
admin.site.register(LOLAggregatedStats)
admin.site.register(SC2Career)
admin.site.register(Terran)
admin.site.register(Zerg)
admin.site.register(Protoss)
admin.site.register(SwarmLevels)
admin.site.register(Campaign)
admin.site.register(Season)
admin.site.register(RewardsList)
admin.site.register(UserCategoryPoints)
admin.site.register(UserAchievementPoints)
admin.site.register(UserAchievement)
admin.site.register(UserAchievementList)
admin.site.register(SC2GameData)
admin.site.register(Achievement)
admin.site.register(Category)
admin.site.register(ChildCategory)

