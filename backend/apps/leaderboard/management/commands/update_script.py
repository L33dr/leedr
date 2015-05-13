from django.core.management.base import BaseCommand

from apps.leaderboard.models import UserProfile
from apps.leaderboard.models import UserGameProfile
from leaderboard.settings import LOL_API_KEY

# External Tools
import requests
import yaml

class Command(BaseCommand):
    help = "Use this to update all LOL users data"

    def handle(self, *args, **options):
        def get_summoner_id(summoner_name):
            return yaml.load(requests.get("https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/" +
                                          summoner_name + "?api_key=" + LOL_API_KEY).content)

        profiles = UserGameProfile.objects.filter(game_id=1)
        print profiles

        for profile in profiles:
            print get_summoner_id(profile.game_user_name)
