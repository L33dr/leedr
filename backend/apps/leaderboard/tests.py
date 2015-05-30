import json

from django.core.urlresolvers import reverse
from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.leaderboard.models import GameDetail, UserProfile, UserGameProfile


@override_settings(EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend')
class GameTestCase(TestCase):
    def setUp(self):
        GameDetail.objects.create(name="League Of Legends", platform="PC", shorthand_name="LOL")
        GameDetail.objects.create(name="Star Craft 2", platform="PC", shorthand_name="SC2")

    def test_game_list_view(self):
        c = Client()
        response = c.get(reverse("game-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
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
        response = c.get(reverse("profile"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_profile_view(self):
        # Setup
        token = Token.objects.get(user_id=1)
        c = Client(HTTP_AUTHORIZATION='Token ' + token.key)

        # Request
        response = c.get(reverse("profile"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
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
        token1 = Token()
        token1.key = token1.generate_key()
        token1.user_id = 1
        token1.created = timezone.now()
        token1.save()

    def test_to_str(self):
        game_profile = UserGameProfile.objects.get(pk=1)
        self.assertEqual(str(game_profile), "asmithgameprofile's LOL profile")

    def test_get_profile_with_games(self):
        # Setup
        token = Token.objects.get(user_id=1)
        c = Client(HTTP_AUTHORIZATION='Token ' + token.key)

        response = c.get(reverse("profile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = [{"premium": False,
                     "user": {"username": "asmith", "email": "", "first_name": "Alice", "last_name": "Smith"},
                     "games": [{"game":
                         {
                             "id": 1,
                             "name": "League Of Legends",
                             "platform": "PC",
                             "shorthand_name": "LOL"
                         },
                         "game_user_name": "asmithgameprofile",
                         "region": "na",
                         "external_user_id": None
                     }]}]
        expected = json.dumps(expected)
        self.assertJSONEqual(response.content, expected)

    def test_post_to_create_game_profile_failure_on_duplicate(self):
        token = Token.objects.get(user_id=1)
        c = APIClient(HTTP_AUTHORIZATION='Token ' + token.key)
        expected = dict({"game":
            {
                "name": "League Of Legends",
                "platform": "PC",
                "thumbnail": "",
                "shorthand_name": "LOL",
                "url": "/leedr/LOL/user-data"
            },
            "game_user_name": "asmithgameprofile",
            "region": "na",
            "external_user_id": None
        })

        response = c.post(reverse("game-profile"), expected, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, '"You cannot have two profiles for the same game, yet!"')
        self.assertEqual(UserGameProfile.objects.count(), 1)

    def test_post_to_create_game_profile(self):
        # Remove the existing game profile so we can re-create it and test the create function.
        game_profile = UserGameProfile.objects.get(pk=1)
        game_profile.delete()

        token = Token.objects.get(user_id=1)
        c = APIClient(HTTP_AUTHORIZATION='Token ' + token.key)
        expected = dict({"game":
            {
                "name": "League Of Legends",
                "platform": "PC",
                "shorthand_name": "LOL",
            },
            "game_user_name": "asmithgameprofile",
            "region": "na",
            'external_user_id': None
        })

        response = c.post(reverse("game-profile"), expected, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertJSONEqual(response.content, expected)

        game_profile = UserGameProfile.objects.get(pk=2)
        game = GameDetail.objects.get(pk=1)

        self.assertEqual(game_profile.user.user.username, "asmith")
        self.assertEqual(game_profile.external_user_id, None)
        self.assertEqual(game_profile.updates_on_demand, 1)
        self.assertEqual(game_profile.game, game)
        self.assertEqual(game_profile.is_in_error_state, False)
        self.assertEqual(game_profile.region, "na")

    def test_post_to_create_second_game_profile_same_user(self):
        token = Token.objects.get(user_id=1)
        game = GameDetail.objects.create(name="Star Craft 2", platform="PC", shorthand_name="SC2")

        c = APIClient(HTTP_AUTHORIZATION='Token ' + token.key)
        expected = dict({"game":
            {
                "name": "Star Craft 2",
                "platform": "PC",
                "shorthand_name": "SC2",
            },
            "game_user_name": "asmithgameprofile",
            "region": "1",
            "external_user_id": 999000
        })

        response = c.post(reverse("game-profile"), expected, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertJSONEqual(response.content, expected)

        game_profile = UserGameProfile.objects.get(game=game)

        self.assertEqual(game_profile.user.user.username, "asmith")
        self.assertEqual(game_profile.external_user_id, 999000)
        self.assertEqual(game_profile.updates_on_demand, 1)
        self.assertEqual(game_profile.game, game)
        self.assertEqual(game_profile.is_in_error_state, False)
        self.assertEqual(game_profile.region, "1")

        self.assertEqual(UserGameProfile.objects.count(), 2)


