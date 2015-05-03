from rest_framework.serializers import ModelSerializer
from rest_auth.serializers import UserDetailsSerializer

#######################################################
# Model Imports
#######################################################
from models import GameDetail
from models import UserProfile
from models import UserGameProfile
from django.contrib.auth.models import User


class GameDetailSerializer(ModelSerializer):
    class Meta:
        model = GameDetail


class UserSerializer(ModelSerializer):

    class Meta(UserDetailsSerializer.Meta):
        model = User


class UserProfileSerializer(ModelSerializer):
    user = UserSerializer(required=True, many=False)

    class Meta:
        model = UserProfile
        fields = ('premium', 'user')


class UserGameProfileSerializer(ModelSerializer):
    user = UserProfileSerializer(required=True, many=False)
    game = GameDetailSerializer(required=True, many=False)

    class Meta:
        model = UserGameProfile
        fields = ('user', 'game', 'game_user_name')
