from django.db import models

from apps.leaderboard.models import UserGameProfile

######################################################################
#
# Basic profile information.
# API Information: GET PROFILE /SC2/PROFILE/:ID/:REGION/:NAME/
#
######################################################################


class SC2Career(models.Model):
    primary_race = models.CharField(max_length=200)
    terran_wins = models.IntegerField()
    protoss_wins = models.IntegerField()
    zerg_wins = models.IntegerField()
    highest_1v1_rank = models.CharField(max_length=200)
    highest_team_rank = models.CharField(max_length=200)
    season_total_games = models.IntegerField()
    career_total_games = models.IntegerField()


class Terran(models.Model):
    level = models.IntegerField()
    total_level_xp = models.IntegerField()
    current_level_xp = models.IntegerField()


class Zerg(models.Model):
    level = models.IntegerField()
    total_level_xp = models.IntegerField()
    current_level_xp = models.IntegerField()


class Protoss(models.Model):
    level = models.IntegerField()
    total_level_xp = models.IntegerField()
    current_level_xp = models.IntegerField()


class SwarmLevels(models.Model):
    level = models.IntegerField()
    terran = models.OneToOneField(Terran)
    zerg = models.OneToOneField(Zerg)
    protoss = models.OneToOneField(Protoss)


class Campaign(models.Model):
    """
    Campaign difficulty levels.
    WOL = Wings of Liberty
    HOTS = Heart of the Swarm

    "campaign" : {
        "wol" : "BRUTAL",
        "hots" : "BRUTAL"
    }
    """
    wol = models.CharField(max_length=200)
    hots = models.CharField(max_length=200)


class Season(models.Model):
    season_id = models.IntegerField()
    season_number = models.IntegerField()
    season_year = models.IntegerField()
    total_games_this_season = models.IntegerField()



class RewardsList(models.Model):
    """
    The API provides a list of ID's. Later we can parse through them and get the data using a different API call.

    That data will be stored in a separate class definition.
    """
    selected = models.CommaSeparatedIntegerField(max_length=2500)
    earned = models.CommaSeparatedIntegerField(max_length=2500)


class UserCategoryPoints(models.Model):
    category_id = models.IntegerField()
    points = models.IntegerField()


class UserAchievementPoints(models.Model):
    total_points = models.IntegerField()
    category_points = models.ManyToManyField(UserCategoryPoints)


class UserAchievementList(models.Model):
    """
    This is their total achievement points.
    Each achievement will have a FK back to this class.
    """
    points = models.OneToOneField(UserAchievementPoints)


class UserAchievement(models.Model):
    """
    API gives us an ID, we will have to resolve that later with another api call.
    Using foreign key to relate back to which list it belongs in.
    """
    achievement_id = models.IntegerField()
    completion_date = models.IntegerField()
    user_list = models.ForeignKey(UserAchievementList)


class SC2GameData(models.Model):
    user_game_profile = models.ForeignKey(UserGameProfile)
    time_stamp = models.DateTimeField(auto_now_add=True)
    profile_id = models.IntegerField()
    realm = models.IntegerField()
    display_name = models.CharField(max_length=200)
    clan_name = models.CharField(max_length=200)
    clan_tag = models.CharField(max_length=200)
    profile_path = models.CharField(max_length=200)
    portrait_url = models.URLField()
    career = models.OneToOneField(SC2Career)
    swarm_levels = models.OneToOneField(SwarmLevels)
    campaign = models.OneToOneField(Campaign)
    season = models.OneToOneField(Season)
    rewards = models.ManyToManyField(RewardsList)
    achievements = models.ManyToManyField(UserAchievementList)

    def __str__(self):
        return str(self.user_game_profile) + "'s SC2 Game Data"


####################################################################
#
# From achievements data only. Not used in basic profile data.
# API information: GET ACHIEVEMENTS /SC2/DATA/ACHIEVEMENTS
#
####################################################################


class Achievement(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    achievement_id = models.IntegerField()
    category = models.IntegerField()
    points = models.IntegerField()
    icon = models.URLField()


class Category(models.Model):
    title = models.CharField(max_length=50)
    category_id = models.IntegerField()


class ChildCategory(models.Model):
    title = models.CharField(max_length=50)
    category = models.IntegerField()
    featured_achievement_id = models.IntegerField()
    parent = models.ForeignKey(Category)


