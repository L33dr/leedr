from __future__ import absolute_import

import re
import yaml

from datetime import timedelta
from requests import get

from celery import shared_task
from django.utils import timezone
from apps.leaderboard.models import UserGameProfile
from apps.leaderboard.tasks import check_valid_response
from apps.lol.tasks import camel_case_to_snake_case
from apps.sc2.models import Campaign, SC2Career, Season, SwarmLevels, Zerg, Protoss, Terran, UserCategoryPoints, \
    UserAchievement, UserAchievementPoints, UserAchievementList
from leaderboard.settings import SC2_API_KEY



@shared_task()
def get_SC2_stats(game_profile):

    request_url = "https://us.api.battle.net/sc2/profile/" + str(game_profile.external_user_id) + "/" \
    + str(game_profile.region) + "/" + str(game_profile.game_user_name) + "/?locale=en_US&apikey=" + SC2_API_KEY

    request = get(request_url)

    if check_valid_response(request):
        data = yaml.load(request.content)

        campaign = Campaign()
        campaign.wol = data['campaign']['wol']
        campaign.hots = data['campaign']['hots']
        campaign.save()
        del data['campaign']

        career = SC2Career()
        for key, value in data['career'].iteritems():
            key_renamed = camel_case_to_snake_case(key)
            setattr(career, key_renamed, value)
        career.save()
        del data['career']

        season = Season()
        for key, value in data['season'].iteritems():
            key_renamed = camel_case_to_snake_case(key)
            setattr(season, key_renamed, value)
        season.save()
        del data['season']

        swarm_levels = SwarmLevels()

        zerg = Zerg()
        for key, value in data['swarmLevels']['zerg'].iteritems():
            key_renamed = camel_case_to_snake_case(key)
            setattr(zerg, key_renamed, value)
        zerg.save()

        protoss = Protoss()
        for key, value in data['swarmLevels']['protoss'].iteritems():
            key_renamed = camel_case_to_snake_case(key)
            setattr(protoss, key_renamed, value)
        protoss.save()

        terran = Terran()
        for key, value in data['swarmLevels']['terran'].iteritems():
            key_renamed = camel_case_to_snake_case(key)
            setattr(terran, key_renamed, value)
        terran.save()

        swarm_levels.zerg = zerg
        swarm_levels.protoss = protoss
        swarm_levels.terran = terran
        swarm_levels.level = data['swarmLevels']['level']
        swarm_levels.save()
        del data['swarmLevels']

        category_points = []
        for key, value in data['achievements']['points']['categoryPoints'].iteritems():
            category = UserCategoryPoints()
            category.category_id = key
            category.points = value
            category.save()
            category_points.append(category)

        point_summary = UserAchievementPoints()
        point_summary.total_points = data['achievements']['points']['totalPoints']
        point_summary.save()
        for category in category_points:
                point_summary.category_points.add(category)

        ach_list = UserAchievementList()
        ach_list.points = point_summary
        ach_list.save()

        for achievement in data['achievements']['achievements']:
            ach = UserAchievement()
            ach.completion_date = achievement['completionDate']
            ach.achievement_id = achievement['achievementId']
            ach.user_list = ach_list
            ach.save()
        del data['achievements']

        print data