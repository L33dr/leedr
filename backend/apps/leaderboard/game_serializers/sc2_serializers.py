from rest_framework.serializers import ModelSerializer
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