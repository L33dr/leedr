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


class UserProfile(models.Model):
    """
    Base user profile. This will bind to a registered user and bind all the related data to them.
    The premium field is currently used to filter down data returned to a user in the game views.
    If they are not premium they should only get one result. If they are premium they should get all the results.

    The game profile will contain game specific user identification (Game username, Game user_id, etc).
    """
    user = models.OneToOneField(User)
    premium = models.BooleanField()

    def is_premium(self):
        return self.premium

    def __str__(self):
        return self.user.get_username() + "'s Profile"

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        """Create a matching profile whenever a user object is created."""
        if created:
            profile, new = UserProfile.objects.get_or_create(user=instance, premium=False)


class UserGameProfile(models.Model):
    """
    Used to bind the user profile to each game the user participates in.
    Related name field is for the serializers to relate back to there and get the list of all the games a user has.
    """
    game = models.ForeignKey(GameDetail)
    game_user_name = models.CharField(max_length=100)
    user = models.ForeignKey(UserProfile, related_name="games")
    region = models.CharField(max_length=10)
    external_user_id = models.IntegerField(null=True, blank=True)
    is_in_error_state = models.BooleanField(default=0)

    def __str__(self):
        return self.game_user_name + "'s " + self.game.name + ' profile'


class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    comment = models.CharField(max_length=2000)
    ip_address = models.IPAddressField(default="0.0.0.0")
    date = models.DateField(auto_now_add=True)


