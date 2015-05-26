from rest_framework.serializers import ModelSerializer
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


from apps.leaderboard.serializers import UserGameProfileSerializer

class SC2CareerSerializer(ModelSerializer):
    class Meta:
        model = SC2Career


class TerranSerializer(ModelSerializer):
    class Meta:
        model = Terran


class ZergSerializer(ModelSerializer):
    class Meta:
        model = Zerg


class ProtossSerializer(ModelSerializer):
    class Meta:
        model = Protoss


class SwarmLevelsSerializer(ModelSerializer):
    terran = TerranSerializer(required=True, many=False)
    zerg = ZergSerializer(required=True, many=False)
    protoss = ProtossSerializer(required=True, many=False)

    class Meta:
        model = SwarmLevels


class CampaignSerializer(ModelSerializer):
    class Meta:
        model = Campaign


class SeasonSerializer(ModelSerializer):
    class Meta:
        model = Season


class RewardsListSerializer(ModelSerializer):
    class Meta:
        model = RewardsList


class UserCategoryPointsSerializer(ModelSerializer):
    class Meta:
        model = UserCategoryPoints


class UserAchievementPointsSerializer(ModelSerializer):
    category_points = UserCategoryPointsSerializer(required=True, many=True)

    class Meta:
        model = UserAchievementPoints


class UserAchievementListSerializer(ModelSerializer):
    points = UserAchievementPointsSerializer(required=True, many=False)

    class Meta:
        model = UserAchievementList


class UserAchievementSerializer(ModelSerializer):
    user_list = UserAchievementListSerializer(required=True, many=False)

    class Meta:
        model = UserAchievement

class SC2GameDataSerializer(ModelSerializer):
    user_game_profile = UserGameProfileSerializer(required=True, many=False)
    career = SC2CareerSerializer(required=True, many=False)
    swarm_levels = SwarmLevelsSerializer(required=True, many=False)
    campaign = CampaignSerializer(required=True, many=False)
    rewards = RewardsListSerializer(required=True, many=True)
    achievements = UserAchievementListSerializer(required=True, many=True)

    class Meta:
        model = SC2GameData