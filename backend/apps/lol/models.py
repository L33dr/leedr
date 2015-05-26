from django.db import models

from apps.leaderboard.models import UserGameProfile


class LOLAggregatedStats(models.Model):
    average_node_capture_assist = models.IntegerField(blank=True, null=True)
    max_node_neutralize_assist = models.IntegerField(blank=True, null=True)
    total_minion_kills = models.IntegerField(blank=True, null=True)
    max_champions_killed = models.IntegerField(blank=True, null=True)
    total_champion_kills = models.IntegerField(blank=True, null=True)
    average_champions_killed = models.IntegerField(blank=True, null=True)
    average_num_deaths = models.IntegerField(blank=True, null=True)
    max_node_capture = models.IntegerField(blank=True, null=True)
    max_objective_player_score = models.IntegerField(blank=True, null=True)
    total_neutral_minions_killed = models.IntegerField(blank=True, null=True)
    max_assists = models.IntegerField(blank=True, null=True)
    average_combat_player_score = models.IntegerField(blank=True, null=True)
    max_node_capture_assist = models.IntegerField(blank=True, null=True)
    average_objective_player_score = models.IntegerField(blank=True, null=True)
    max_team_objective = models.IntegerField(blank=True, null=True)
    total_assists = models.IntegerField(blank=True, null=True)
    average_node_capture = models.IntegerField(blank=True, null=True)
    average_total_player_score = models.IntegerField(blank=True, null=True)
    average_team_objective = models.IntegerField(blank=True, null=True)
    average_node_neutralize = models.IntegerField(blank=True, null=True)
    max_node_neutralize = models.IntegerField(blank=True, null=True)
    average_node_neutralize_assist = models.IntegerField(blank=True, null=True)
    average_assists = models.IntegerField(blank=True, null=True)
    max_total_player_score = models.IntegerField(blank=True, null=True)
    max_combat_player_score = models.IntegerField(blank=True, null=True)
    total_turrets_killed = models.IntegerField(blank=True, null=True)
    total_node_neutralize = models.IntegerField(blank=True, null=True)
    total_node_capture = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "LOL Aggregated Stats Object"

    class Meta:
        verbose_name_plural = "LOL Summary Aggregated Stats"


class LOLPlayerStatSummary(models.Model):
    player_stat_summary_type = models.CharField(max_length=100)
    stats = models.OneToOneField(LOLAggregatedStats)
    wins = models.IntegerField(blank=True, null=True)
    losses = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "LOL Player Stat Summary Object"

    class Meta:
        verbose_name_plural = "LOL Player Profile Stat Summaries"


class LOLGameData(models.Model):
    user_game_profile = models.ForeignKey(UserGameProfile)
    time_stamp = models.DateTimeField(auto_now_add=True)
    summoner_id = models.IntegerField()
    player_stat_summary = models.ManyToManyField(LOLPlayerStatSummary)

    def __str__(self):
        return str(self.user_game_profile) + "'s LOL Game Data"

    class Meta:
        verbose_name_plural = "LOL Game Data Profiles"