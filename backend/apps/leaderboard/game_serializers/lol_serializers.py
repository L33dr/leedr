from rest_framework.serializers import ModelSerializer
from rest_auth.serializers import UserDetailsSerializer

#######################################################
# Model Imports
# These may show as unresolved but they work as intended.
#######################################################

from apps.leaderboard.game_models.lol_game_model import LeagueOfLegendsGameData
from apps.leaderboard.game_models.lol_game_model import AggregatedStats
from apps.leaderboard.game_models.lol_game_model import PlayerStatSummary


class AggregatedStatsSerializer(ModelSerializer):
    class Meta:
        model = AggregatedStats


class PlayerStatSummarySerializer(ModelSerializer):
    stats = AggregatedStatsSerializer(many=False, required=True)

    class Meta:
        model = PlayerStatSummary


class LeagueOfLegendsGameDataSerializer(ModelSerializer):
    player_stat_summary = PlayerStatSummarySerializer(many=True, required=True)

    class Meta:
        model = LeagueOfLegendsGameData
        fields = ('player_stat_summary', 'time_stamp', 'summoner_id')
