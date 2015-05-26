from __future__ import absolute_import

import re

import yaml


from datetime import timedelta
from requests import get

from django.core.mail import EmailMessage
from django.utils import timezone
from django.utils.datetime_safe import time
from django.template import Context, loader


from celery import shared_task

from apps.leaderboard.game_models.lol_game_model import LOLPlayerStatSummary, LOLAggregatedStats, LOLGameData
from apps.leaderboard.models import UserGameProfile, GameDetail, UserProfile
from leaderboard.settings import EMAIL_HOST_USER, LOL_API_KEY

"""
Shared tasks can be called throughout the application and ran asynchronously by importing the task name,
then calling taskname.delay(). The delay function will add it into the queue to be processed as soon as possible.

For more information see: https://celery.readthedocs.org/en/latest/userguide/calling.html

You can also call a shared task directly and have it executed in serial by just calling it as if were any other function.
"""


class ServiceUnavailable(Exception):
    pass

def check_valid_response(request):
    """
    :raises NameError: Raised if username is not found on 3rd party API (404)
    :raises Exception: Raised if 400 or 500 error from server.
    :return: True if request has acceptable status code.
    """
    if request.status_code not in [400, 404, 429, 500, 503]:
        return True
    elif request.status_code == 404:
        raise NameError("API returned 404. Name not found or is incorrect")
    elif request.status_code in [429, 503]:
        raise ServiceUnavailable("Status code: {}".format(request.status_code))
    else:
        raise Exception("LOL API returned status code: {} ".format(request.status_code))

def camel_case_to_snake_case(key):
    key_renamed = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', key)
    key_renamed = re.sub('([a-z0-9])([A-Z])', r'\1_\2', key_renamed).lower()
    return key_renamed

@shared_task()
def get_LOL_id_by_username(username, region):
    """
    Returns LOL ID by performing a query on their api by LOL username.
    This would generally be ran right as a user requests we add their game.
    :param username: String.
    :param region: String. Specifying which region they are participating in the game. Only used to gather their info.
    :return: Integer
    """
    username = username.lower()
    request_URL = 'https://' + region + '.api.pvp.net/api/lol/' + region + '/v1.4/summoner/by-name/' + \
                  username + '?api_key=' + LOL_API_KEY
    request = get(request_URL)
    if check_valid_response(request):
        data = yaml.load(request.content)
        return data[username]['id']


@shared_task()
def send_contact_request_reply_task(first_name, email):
    """

    """
    template = loader.get_template('leaderboard/email.html')
    context = Context({"first_name": first_name})
    message = template.render(context)

    subject = "Thank you for submitting the form."
    from_emails = EMAIL_HOST_USER
    msg = EmailMessage(subject, message, from_emails, [email])
    msg.content_subtype = "html"
    msg.send()


@shared_task()
def send_contact_request_alert_task(first_name, reply_email, comment, ip_address):
    """
    Alerting the admin that there was a new comment.
    """
    subject = "New contact request."
    from_email = EMAIL_HOST_USER
    message = "<html>A new contact requests has been submitted. <br><br>Name: {}<br>Email: {}<br>Message: {}" \
              "<br>IP Address: {}<br></html>".format(first_name, reply_email, comment, ip_address)
    msg = EmailMessage(subject, message, from_email, [EMAIL_HOST_USER])
    msg.content_subtype = 'html'
    msg.send()


@shared_task()
def get_stats_by_id(user_id, game_profile):
    """
    """

    # Make request to external API and parse data into python dict
    request_url = 'https://' + game_profile.region + '.api.pvp.net/api/lol/' +\
                  game_profile.region + '/v1.3/stats/by-summoner/' + str(user_id) + \
                  '/summary?season=SEASON2015&api_key=' + LOL_API_KEY
    request = get(request_url)

    if check_valid_response(request):
        data = yaml.load(request.content)
        if 'playerStatSummaries' in data:
            # Setup list of player stat summaries to be used in the game_data
            player_stat_summaries = []

            for summary in data['playerStatSummaries']:
                player_summary = LOLPlayerStatSummary()
                player_summary.wins = summary['wins']
                player_summary.player_stat_summary_type = summary['playerStatSummaryType']
                if 'losses' in summary:
                    player_summary.losses = summary['losses']

                agg_stats = LOLAggregatedStats()
                for key, value in summary['aggregatedStats'].iteritems():
                    key_renamed = camel_case_to_snake_case(key)
                    setattr(agg_stats, key_renamed, value)
                agg_stats.save()

                player_summary.stats = agg_stats
                player_summary.save()
                player_stat_summaries.append(player_summary)

            game_data = LOLGameData()
            game_data.summoner_id = user_id
            game_data.user_game_profile = game_profile
            game_data.save()
            for summary in player_stat_summaries:
                game_data.player_stat_summary.add(summary)

@shared_task()
def find_LOL_users_to_update():
    game = GameDetail.objects.get(shorthand_name='LOL')
    game_profiles = UserGameProfile.objects.filter(game=game).all()
    next_update_time = timezone.now()
    for game_profile in game_profiles:
        user_id = 0
        if game_profile.is_in_error_state:
            print "In Error State: {}".format(game_profile)
            continue
        if not game_profile.external_user_id:
            try:
                user_id = get_LOL_id_by_username(game_profile.game_user_name, game_profile.region)
                game_profile.external_user_id = user_id
            except NameError as e:
                game_profile.is_in_error_state = True
                continue
            except ServiceUnavailable as e:
                print e
                time.sleep(30)
                continue
            except Exception as e:
                print e
            game_profile.save()
        else:
            user_id = game_profile.external_user_id
        get_stats_by_id.apply_async((user_id, game_profile), eta=next_update_time)
        next_update_time += timedelta(seconds=2.5)


@shared_task()
def give_updates_on_demand():
    """
    This task should be ran daily to give users their updates on demand.
    If they are premium they will get 5 daily, else they will get 1 daily.
    These updates are PER GAME PROFILE. Each game a user plays will get their own updates on demand.
    """
    game_profiles = UserGameProfile.objects.filter(is_in_error_state=False).all()
    print game_profiles
    for profile in game_profiles:
        if profile.user.is_premium():
            print profile.updates_on_demand
            profile.updates_on_demand = 5
        else:
            print profile.updates_on_demand
            profile.updates_on_demand = 1
        profile.save()
