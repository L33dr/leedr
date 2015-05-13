from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class GameDetail(models.Model):
    """
    This is the actual game definition. Should only have one instance per game per platform.
    """
    name = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    thumbnail = models.URLField()
    shorthand_name = models.CharField(max_length=10)

    def __str__(self):
        return self.name + ' on ' + self.platform


class UserGameProfile(models.Model):
    """
    Used to bind the user profile to each game the user participates in.
    """
    game = models.ForeignKey(GameDetail)
    game_user_name = models.CharField(max_length=100)

    def __str__(self):
        return self.game_user_name + "'s " + self.game.name + ' profile'

class UserProfile(models.Model):
    """
    Base user profile. This will bind to a registered user and bind all the related data to them.
    Premium field is not yet used. Will be implemented later as a paid service.
    """
    user = models.OneToOneField(User)
    premium = models.BooleanField()
    games = models.ManyToManyField(UserGameProfile)

    def __str__(self):
        return self.user.get_username() + "'s Profile"

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a matching profile whenever a user object is created."""
    if created:
        profile, new = UserProfile.objects.get_or_create(user=instance, premium=False)
