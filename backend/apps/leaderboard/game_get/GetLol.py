import datetime
import urllib
import time
import base64
import json
import unicodedata
import requests
import yaml


# Script will stop after 100 profiles.
added = 0

api_key = '70b12d3a-d1b4-4375-b33a-fbd34e815056'

def get_profile(request):
    profile_data = requests.get('https://na.api.pvp.net/api/lol/na/v1.4/summoner/lol/{}?api_key{}' .format(lol_profile, api_key))


