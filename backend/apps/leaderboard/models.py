from django.contrib.auth.models import User
from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)


class UserGameProfile(models.Model):
    game = models.ForeignKey(Game)
    game_user_name = models.CharField(max_length=100)


class LeagueOfLegendsGameData(models.Model):
    user_game_profile = models.ForeignKey(UserGameProfile)
    time_stamp = models.DateTimeField()
    kills = models.IntegerField()
    deaths = models.IntegerField()
    wins = models.IntegerField()
    losses = models.IntegerField()


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    games = models.ManyToManyField(UserGameProfile)
    premium = models.BooleanField()