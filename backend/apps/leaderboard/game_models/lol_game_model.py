from django.db import models

from apps.leaderboard.models import UserGameProfile


class LOLAggregatedStats(models.Model):
    average_node_capture_assist = models.IntegerField()
    max_node_neutralize_assist = models.IntegerField()
    total_minion_kills = models.IntegerField()
    max_champions_killed = models.IntegerField()
    total_champion_kills = models.IntegerField()
    average_champions_killed = models.IntegerField()
    average_num_deaths = models.IntegerField()
    max_node_capture = models.IntegerField()
    max_objective_player_score = models.IntegerField()
    total_neutral_minions_killed = models.IntegerField()
    max_assists = models.IntegerField()
    average_combat_player_score = models.IntegerField()
    max_node_capture_assist = models.IntegerField()
    average_objective_player_score = models.IntegerField()
    max_team_objective = models.IntegerField()
    total_assists = models.IntegerField()
    average_node_capture = models.IntegerField()
    average_total_player_score = models.IntegerField()
    average_team_objective = models.IntegerField()
    average_node_neutralize = models.IntegerField()
    max_node_neutralize = models.IntegerField()
    average_node_neutralize_assist = models.IntegerField()
    average_assists = models.IntegerField()
    max_total_player_score = models.IntegerField()
    max_combat_player_score = models.IntegerField()
    total_turrets_killed = models.IntegerField()
    total_node_neutralize = models.IntegerField()
    total_node_capture = models.IntegerField()

    def __str__(self):
        return "LOL Aggregated Stats Object"

    class Meta:
        verbose_name_plural = "LOL Summary Aggregated Stats"


class LOLPlayerStatSummary(models.Model):
    player_stat_summary_type = models.CharField(max_length=100)
    stats = models.OneToOneField(LOLAggregatedStats)
    wins = models.IntegerField()
    losses = models.IntegerField()

    def __str__(self):
        return "LOL Player Stat Summary Object"

    class Meta:
        verbose_name_plural = "LOL Player Profile Stat Summaries"


class LOLGameData(models.Model):
    user_game_profile = models.ForeignKey(UserGameProfile)
    time_stamp = models.DateTimeField()
    summoner_id = models.IntegerField()
    player_stat_summary = models.ManyToManyField(LOLPlayerStatSummary)

    def __str__(self):
        return str(self.user_game_profile) + "'s LOL Game Data"

    class Meta:
        verbose_name_plural = "LOL Game Data Profiles"