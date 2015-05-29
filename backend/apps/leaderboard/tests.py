import json

from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.authtoken.models import Token

from apps.leaderboard.models import GameDetail, UserProfile, UserGameProfile


@override_settings(EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend')
class GameTestCase(TestCase):
    def setUp(self):
        GameDetail.objects.create(name="League Of Legends", platform="PC", shorthand_name="LOL")
        GameDetail.objects.create(name="Star Craft 2", platform="PC", shorthand_name="SC2")

    def test_game_list_view(self):
        c = Client()
        response = c.get('/leedr/game-list/')
        self.assertEqual(response.status_code, 200)
        expected = [{"id": 1, "name": "League Of Legends",
                     "platform": "PC", "shorthand_name": "LOL"},
                    {"id": 2, "name": "Star Craft 2",
                     "platform": "PC", "shorthand_name": "SC2"}]
        expected_json = json.dumps(expected)
        self.assertJSONEqual(response.content, expected_json)

    def test_to_str_method(self):
        game1 = GameDetail.objects.get(pk=1)
        game2 = GameDetail.objects.get(pk=2)
        self.assertEqual(str(game1), "League Of Legends on PC")
        self.assertEqual(str(game2), "Star Craft 2 on PC")


class UserProfileTestCase(TestCase):
    def setUp(self):
        User.objects.create(first_name="Alice", last_name="Smith", username="asmith")
        User.objects.create(first_name="Bob", last_name="Smith", username="bsmith")
        token1 = Token()
        token1.key = token1.generate_key()
        token1.user_id = 1
        token1.created = timezone.now()
        token1.save()
        token2 = Token()
        token2.key = token2.generate_key()
        token2.user_id = 2
        token2.created = timezone.now()
        token2.save()

    def test_auto_profile_creation(self):
        self.assertEqual(UserProfile.objects.count(), 2)

    def test_to_str(self):
        profile = UserProfile.objects.get(pk=1)
        self.assertEqual(str(profile), "asmith's Profile")

    def test_profile_is_not_premium_on_create(self):
        profile = UserProfile.objects.get(pk=1)
        self.assertEqual(profile.is_premium(), False)

    def test_user_profile_view_requires_auth(self):
        c = Client()
        response = c.get("/leedr/user-profile/")
        self.assertEqual(response.status_code, 401)

    def test_user_profile_view(self):
        # Setup
        token = Token.objects.get(user_id=1)
        c = Client(HTTP_AUTHORIZATION='Token ' + token.key)

        # Request
        response = c.get("/leedr/user-profile/")

        self.assertEqual(response.status_code, 200)
        expected = [{"premium": False, "user":
                    {"username": "asmith", "email": "", "first_name": "Alice", "last_name": "Smith"},
                     "games": []}]
        expected = json.dumps(expected)
        self.assertJSONEqual(response.content, expected)


class UserGameProfileTests(TestCase):
    def setUp(self):
        game = GameDetail.objects.create(name="League Of Legends", platform="PC", shorthand_name="LOL")
        user = User.objects.create(first_name="Alice", last_name="Smith", username="asmith")
        user_profile = UserProfile.objects.get(user=user)
        UserGameProfile.objects.create(game=game,
                                       game_user_name="asmithgameprofile",
                                       user=user_profile,
                                       region="na")

    def test_to_str(self):
        game_profile = UserGameProfile.objects.get(pk=1)
        self.assertEqual(str(game_profile), "asmithgameprofile's LOL profile")
