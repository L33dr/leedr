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
    game = GameDetailSerializer(required=True, many=False)

    class Meta:
        model = UserGameProfile
        fields = ('game', 'game_user_name')

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
        user = User.objects.get(username=username)
        print user
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.update(user, user_data)

        # update games some how

        instance.save()
        return instance

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment