from rest_framework.serializers import ModelSerializer
from apps.leaderboard.game_models.lol_game_model import LOLGameData
from apps.leaderboard.game_models.lol_game_model import LOLAggregatedStats
from apps.leaderboard.game_models.lol_game_model import LOLPlayerStatSummary


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