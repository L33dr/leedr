from rest_framework.serializers import ModelSerializer
from apps.lol.models import LOLGameData, LOLAggregatedStats, LOLPlayerStatSummary


class AggregatedStatsSerializer(ModelSerializer):
    class Meta:
        model = LOLAggregatedStats


class PlayerStatSummarySerializer(ModelSerializer):
    stats = AggregatedStatsSerializer(many=False, required=True)

    class Meta:
        model = LOLPlayerStatSummary


class LeagueOfLegendsGameDataSerializer(ModelSerializer):
    player_stat_summary = PlayerStatSummarySerializer(many=True, required=True)

    class Meta:
        model = LOLGameData
        fields = ('player_stat_summary', 'time_stamp', 'summoner_id')