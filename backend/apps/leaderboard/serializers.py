from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_auth.serializers import UserDetailsSerializer

#######################################################
# Model Imports
#######################################################
from backend.apps.leaderboard.models import Game


class GameSerializer(ModelSerializer):
    class Meta:
        model = Game


class UserSerializer(UserDetailsSerializer):
    premium = serializers.BooleanField(source="userprofile.premium")

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('premium')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userpfoile', {})
        premium = profile_data.get('premium')

        instance = super(UserSerializer, self).update(instance, validated_data)

        # get and update user profile
        profile = instance.userprofile
        if profile_data and premium:
            profile.premium = premium
            profile.save()
        return instance
