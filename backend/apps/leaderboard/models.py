from django.contrib.auth.models import User
from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)


class UserGameProfile(models.Model):
    game = models.ForeignKey(Game)
    game_user_name = models.CharField(max_length=100)
    game_user_id = models.IntegerField()


class LeagueOfLegendsGameData(models.Model):
    user_game_profile = models.ForeignKey(UserGameProfile)
    time_stamp = models.DateTimeField()
    summoner_level = models.IntegerField()
    total_champion_kills = models.IntegerField()
    total_assists = models.IntegerField()
    total_turrets_killed = models.IntegerField()
    total_minions_killed = models.IntegerField()
    avg_assists = models.IntegerField()
    avg_champion_kills = models.IntegerField()
    avg_deaths = models.IntegerField()
    wins = models.IntegerField()


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    games = models.ManyToManyField(UserGameProfile)
    premium = models.BooleanField()