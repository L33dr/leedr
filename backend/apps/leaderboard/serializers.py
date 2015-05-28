from rest_framework.serializers import ModelSerializer
from rest_auth.serializers import UserDetailsSerializer

#######################################################
# Model Imports
#######################################################
from models import GameDetail
from models import UserProfile
from models import UserGameProfile
from models import Comment
from django.contrib.auth.models import User



class GameDetailSerializer(ModelSerializer):
    class Meta:
        model = GameDetail


class UserSerializer(ModelSerializer):

    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        read_only_fields = ('email', 'username')


class UserGameProfileSerializer(ModelSerializer):
    game = GameDetailSerializer(many=False, read_only=False)

    class Meta:
        model = UserGameProfile
        fields = ('game', 'game_user_name', 'region')

    def create(self, validated_data, user, game):
        try:
            exists = UserGameProfile.objects.filter(game=game, user=user).get().id
        except UserGameProfile.DoesNotExist:
            game = GameDetail.objects.filter(shorthand_name=game.shorthand_name).first()
            profile = UserGameProfile()
            profile.game = game
            profile.user = user
            profile.game_user_name = self.data['game_user_name']
            profile.region = self.data['region']
            profile.save()
            return profile
        else:
            raise ValueError

class UserProfileSerializer(ModelSerializer):
    user = UserSerializer(required=True, many=False)
    games = UserGameProfileSerializer(required=False, many=True)

    class Meta:
        model = UserProfile
        fields = ('premium', 'user', 'games')
        read_only_fields = ('premium', )

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        game_data = validated_data.pop('games')
        username = self.data['user']['username']

        # Querying for the current user object. Will be used to update the user object defined by django.
        user = User.objects.get(username=username)
        # Creating a new serializer, this is so we can validate the data and call update
        # and do the actual updating of the user object.
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.update(user, user_data)

        # TODO: Update games

        instance.save()
        return instance

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment