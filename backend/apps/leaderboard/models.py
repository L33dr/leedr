from django.contrib.auth.models import User
from django.db import models


class GameDetail(models.Model):
    """
    This is the actual game definition. Should only have one instance per game per platform.
    """
    name = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)

    def __str__(self):
        return self.name + ' on ' + self.platform



class UserProfile(models.Model):
    """
    Base user profile. This will bind to a registered user and bind all the related data to them.
    Premium field is not yet used. Will be implemented later as a paid service.
    """
    user = models.OneToOneField(User)

    premium = models.BooleanField()

    def __str__(self):
        return self.user.get_username() + "'s Profile"


class UserGameProfile(models.Model):
    """
    Used to bind the user profile to each game the user participates in.
    """
    game = models.ForeignKey(GameDetail)
    user = models.ForeignKey(UserProfile)
    game_user_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user.user.get_username() + "'s " + self.game.name + ' profile'


