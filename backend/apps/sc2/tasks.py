from __future__ import absolute_import
from datetime import timedelta
from django.utils import timezone

import yaml
from requests import get
from celery import shared_task
from apps.leaderboard.models import GameDetail, UserGameProfile

from apps.leaderboard.tasks import check_valid_response
from apps.lol.tasks import camel_case_to_snake_case
from apps.sc2.models import Campaign, SC2Career, Season, SwarmLevels, Zerg, Protoss, Terran, UserCategoryPoints, \
    UserAchievement, UserAchievementPoints, UserAchievementList, SC2GameData, RewardsList
from leaderboard.settings import SC2_API_KEY


@shared_task()
def get_SC2_stats(game_profile):

    request_url = "https://us.api.battle.net/sc2/profile/" + str(game_profile.external_user_id) + "/" \
    + str(game_profile.region) + "/" + str(game_profile.game_user_name) + "/?locale=en_US&apikey=" + SC2_API_KEY

    request = get(request_url)

    valid = check_valid_response(request)
    print valid
    if valid:
        data = yaml.load(request.content)

        campaign = Campaign()
        campaign.wol = data['campaign']['wol']
        campaign.hots = data['campaign']['hots']
        campaign.save()

        career = SC2Career()
        for key, value in data['career'].iteritems():
            key_renamed = camel_case_to_snake_case(key)
            setattr(career, key_renamed, value)
        career.save()

        season = Season()
        for key, value in data['season'].iteritems():
            key_renamed = camel_case_to_snake_case(key)
            setattr(season, key_renamed, value)
        season.save()

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

        rewards = RewardsList()
        if 'rewards' in data:
            if 'selected' in data['rewards']:
                rewards.selected = data['rewards']['selected']
            if 'earned' in data['rewards']:
                rewards.earned = data['rewards']['earned']
        rewards.save()

        game_data = SC2GameData()
        game_data.display_name = data['displayName']
        game_data.realm = data['realm']
        game_data.profile_id = data['id']
        game_data.clan_name = data['clanName']
        game_data.clan_tag = data['clanTag']
        game_data.profile_path = data['profilePath']
        game_data.portrait_url = data['portrait']['url']

        game_data.user_game_profile = game_profile
        game_data.career = career
        game_data.swarm_levels = swarm_levels
        game_data.campaign = campaign
        game_data.season = season
        game_data.achievements = ach_list
        game_data.save()

        game_data.rewards.add(rewards)
        game_data.save()
        return True
    else:
        return False

@shared_task()
def find_SC2_users_to_update():
    game = GameDetail.objects.get(shorthand_name='SC2')
    game_profiles = UserGameProfile.objects.filter(game=game)
    next_update_time = timezone.now()
    for game_profile in game_profiles:
        if game_profile.is_in_error_state:
            print "In Error State: {}".format(game_profile)
            continue
        try:
            get_SC2_stats.apply_async((game_profile,), eta=next_update_time)
        except NameError:
            game_profile.is_in_error_state = True
            game_profile.save()
        finally:
            next_update_time += timedelta(milliseconds=200)

