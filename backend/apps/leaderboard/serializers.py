from rest_framework.serializers import ModelSerializer
from rest_auth.serializers import UserDetailsSerializer

#######################################################
# Model Imports
#######################################################
from models import GameDetail
from models import UserProfile
from django.contrib.auth.models import User


class GameDetailSerializer(ModelSerializer):
    class Meta:
        model = GameDetail


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('premium',)


class UserSerializer(ModelSerializer):
    profile = UserProfileSerializer(required=False, many=False)

    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = UserDetailsSerializer.Meta.fields + ('profile',)
