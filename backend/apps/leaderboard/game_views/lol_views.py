"""
Base views for LOL.
"""
from rest_framework import generics
from apps.leaderboard.game_models.lol_game_model import LOLAggregatedStats, LOLGameData
from apps.leaderboard.game_serializers.lol_serializers import AggregatedStatsSerializer, \
    LeagueOfLegendsGameDataSerializer


class LOLStatsById(generics.RetrieveAPIView):
    serializer_class = AggregatedStatsSerializer
    queryset = LOLAggregatedStats.objects.all()


class LOLAllStats(generics.ListAPIView):
    serializer_class = LeagueOfLegendsGameDataSerializer
    queryset = LOLGameData.objects.all()

# class LOLStatSummary(generics.)