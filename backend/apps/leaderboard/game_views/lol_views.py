"""
Base views for LOL.
"""
from rest_framework import generics
from apps.leaderboard.game_models.lol_game_model import LOLAggregatedStats, LOLGameData
from apps.leaderboard.game_serializers.lol_serializers import AggregatedStatsSerializer, \
    LeagueOfLegendsGameDataSerializer
from rest_framework import authentication, permissions


class LOLStatsById(generics.RetrieveAPIView):
    serializer_class = AggregatedStatsSerializer
    queryset = LOLAggregatedStats.objects.all()

class LOLAllStats(generics.ListAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LeagueOfLegendsGameDataSerializer

    def get_queryset(self):
        return LOLGameData.objects.filter(user_game_profile__userprofile__user=self.request.user).all()


# class LOLStatSummary(generics.)