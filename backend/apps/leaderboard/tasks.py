from __future__ import absolute_import
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from requests import get
import yaml
from apps.leaderboard.game_models.lol_game_model import LOLPlayerStatSummary, LOLAggregatedStats
from apps.leaderboard.models import UserGameProfile, UserProfile, GameDetail
from leaderboard.settings import EMAIL_HOST_USER, LOL_API_KEY
from django.template import Context, loader
from celery import shared_task
from apps.leaderboard.game_models import lol_game_model

"""
Shared tasks can be called throughout the application and ran asynchronously by importing the task name,
then calling taskname.delay(). The delay function will add it into the queue to be processed as soon as possible.

For more information see: https://celery.readthedocs.org/en/latest/userguide/calling.html

You can also call a shared task directly and have it executed in serial by just calling it as if were any other function.
"""


class ServiceUnavailable(Exception):
    pass


def get_LOL_id_by_username(username, region):
    """
    Returns LOL ID by performing a query on their api by LOL username.
    This would generally be ran right as a user requests we add their game.
    :param username: String.
    :param region: String. Specifying which region they are participating in the game. Only used to gather their info.
    :return: Integer
    :raises NameError: Raised if username is not found on 3rd party API (404)
    :raises Exception: Raised if 400 or 500 error from server.
    """
    username = username.lower()
    request_URL = 'https://' + region + '.api.pvp.net/api/lol/' + region + '/v1.4/summoner/by-name/' + \
                  username + '?api_key=' + LOL_API_KEY
    request = get(request_URL)
    if request.status_code not in [400, 404, 429, 500, 503]:
        data = yaml.load(request.content)
        return data[username]['id']
    elif request.status_code == 404:
        raise NameError("API returned 404. Name not found or is incorrect")
    elif request.status_code in [429, 503]:
        raise ServiceUnavailable("Status code: {}".format(request.status_code))
    else:
        raise Exception("LOL API returned status code: {} ".format(request.status_code))


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
def get_stats_by_id(id, region, user):
    """
    """
    user = User.objects.get(username='t')
    user_profile = UserProfile.objects.get(user=user)
    game = GameDetail.objects.get(shorthand_name="LOL")
    game_profile = UserGameProfile.objects.get(user=user_profile, game=game)
    request_url = 'https://' + region + '.api.pvp.net/api/lol/' + region + '/v1.3/stats/by-summoner/' + str(id) + \
                  '/summary?season=SEASON2015&api_key=' + LOL_API_KEY
    request = get(request_url)
    data = yaml.load(request.content)

    player_stat_summaries = []

    for summary in data['playerStatSummaries']:
        wins = summary['wins']
        stats = {
        'average_node_capture_assist': summary['aggregatedStats']['averageNodeCaptureAssist'],
        'max_node_neutralize_assist': summary['aggregatedStats']['maxNodeNeutralizeAssist'],
        'total_minion_kills':  summary['aggregatedStats']['totalMinionKills'],
        'max_champions_killed': summary['aggregatedStats']['maxChampionsKilled'],
        'total_champion_kills': summary['aggregatedStats']['totalChampionKills'],
        'average_champions_killed': summary['aggregatedStats']['averageChampionsKilled'],
        'average_num_deaths': summary['aggregatedStats']['averageNumDeaths'],
        'max_node_capture': summary['aggregatedStats']['maxNodeCapture'],
        'max_objective_player_score': summary['aggregatedStats']['maxObjectivePlayerScore'],
        'total_neutral_minions_killed': summary['aggregatedStats']['totalNeutralMinionsKilled'],
        'max_assists': summary['aggregatedStats']['maxAssists'],
        'average_combat_player_score': summary['aggregatedStats']['averageCombatPlayerScore'],
        'max_node_capture_assist': summary['aggregatedStats']['maxNodeCaptureAssist'],
        'average_objective_player_score': summary['aggregatedStats']['averageObjectivePlayerScore'],
        'max_team_objective': summary['aggregatedStats']['maxTeamObjective'],
        'total_assists': summary['aggregatedStats']['totalAssists'],
        'average_node_capture': summary['aggregatedStats']['averageNodeCapture'],
        'average_total_player_score': summary['aggregatedStats']['averageTotalPlayerScore'],
        'average_team_objective': summary['aggregatedStats']['averageTeamObjective'],
        'average_node_neutralize': summary['aggregatedStats']['averageNodeNeutralize'],
        'max_node_neutralize': summary['aggregatedStats']['maxNodeNeutralize'],
        'average_node_neutralize_assist ': summary['aggregatedStats']['averageNodeNeutralizeAssist'],
        'average_assists': summary['aggregatedStats']['averageAssists'],
        'max_total_player_score': summary['aggregatedStats']['maxTotalPlayerScore'],
        'max_combat_player_score': summary['aggregatedStats']['maxCombatPlayerScore'],
        'total_turrets_killed': summary['aggregatedStats']['totalTurretsKilled'],
        'total_node_neutralize': summary['aggregatedStats']['totalNodeNeutralize'],
        'total_node_capture': summary['aggregatedStats']['totalNodeCapture']
        }
        agg_stats = LOLAggregatedStats()
        for k, v in stats.items():
            LOLAggregatedStats.k = v
        agg_stats.save()


        stat_sum = LOLPlayerStatSummary(wins=wins, stats=agg_stats)


    game_data = lol_game_model.LOLGameData(data, user_game_profile=game_profile, summoner_id=id,
                                           player_stat_summary=data['playerStatSummaries'])
    print game_data
    # game_data.save()
    print game_data.player_stat_summary

