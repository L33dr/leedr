"""
Base views for SC2.
"""
from rest_framework import generics
from rest_framework import authentication, permissions
from apps.sc2.models import SC2Career,\
    Terran, Zerg, Protoss, SwarmLevels, Campaign, Season, RewardsList,\
    UserCategoryPoints, UserAchievementPoints, UserAchievementList,\
    UserAchievement, SC2GameData
from apps.sc2.serializers import SC2CareerSerializer,\
    TerranSerializer, ZergSerializer, ProtossSerializer, SwarmLevelsSerializer,\
    CampaignSerializer, SeasonSerializer, RewardsListSerializer, UserCategoryPointsSerializer,\
    UserAchievementPointsSerializer, UserAchievementListSerializer,\
    UserAchievementSerializer, SC2GameDataSerializer
from apps.leaderboard.models import UserProfile


class SC2CareerView(generics.RetrieveAPIView):
    serializer_class = SC2CareerSerializer
    queryset = SC2Career.objects.all()


class TerranView(generics.RetrieveAPIView):
    serializer_class = TerranSerializer
    queryset = Terran.objects.all()


class ZergView(generics.RetrieveAPIView):
    serializer_class = ZergSerializer
    queryset = Zerg.objects.all()


class ProtossView(generics.RetrieveAPIView):
    serializer_class = ProtossSerializer
    queryset = Protoss.objects.all()


class SwarmLevelsView(generics.RetrieveAPIView):
    serializer_class = SwarmLevelsSerializer
    queryset = SwarmLevels.objects.all()


class CampaignView(generics.RetrieveAPIView):
    serializer_class = CampaignSerializer
    queryset = Campaign.objects.all()


class SeasonView(generics.RetrieveAPIView):
    serializer_class = SeasonSerializer
    queryset = Season.objects.all()


class RewardsListView(generics.RetrieveAPIView):
    serializer_class = RewardsListSerializer
    queryset = RewardsList.objects.all()


class UserCategoryPointsView(generics.RetrieveAPIView):
    serializer_class = UserCategoryPointsSerializer
    queryset = UserCategoryPoints.objects.all()


class UserAchievementPointsView(generics.RetrieveAPIView):
    serializer_class = UserAchievementPointsSerializer
    queryset = UserAchievementPoints.objects.all()


class UserAchievementListView(generics.RetrieveAPIView):
    serializer_class = UserAchievementListSerializer
    queryset = UserAchievementList.objects.all()


class UserAchievementView(generics.RetrieveAPIView):
    serializer_class = UserAchievementSerializer
    queryset = UserAchievement.objects.all()


class SC2GameDataView(generics.ListAPIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SC2GameDataSerializer

    def get_queryset(self):
        is_premium = UserProfile.objects.filter(user=self.request.user).first().is_premium()
        data = SC2GameData.objects.filter(user_game_profile__user__user=self.request.user).order_by("-time_stamp")
        # Non-premium members only get the first result
        if data.first():
            if is_premium:
                return data.all()
            else:
                # Needs to return a list type
                return [data.first(), ]
        else:
            return None
