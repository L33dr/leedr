from django.contrib import admin
from apps.sc2.models import SC2Career
from apps.sc2.models import Terran
from apps.sc2.models import Zerg
from apps.sc2.models import Protoss
from apps.sc2.models import SwarmLevels
from apps.sc2.models import Campaign
from apps.sc2.models import Season
from apps.sc2.models import RewardsList
from apps.sc2.models import UserCategoryPoints
from apps.sc2.models import UserAchievementPoints
from apps.sc2.models import UserAchievement
from apps.sc2.models import UserAchievementList
from apps.sc2.models import SC2GameData
from apps.sc2.models import Achievement
from apps.sc2.models import Category
from apps.sc2.models import ChildCategory

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
