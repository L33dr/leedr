"""
Base views for LOL.
"""
from rest_framework import generics
from apps.lol.models import LOLAggregatedStats, LOLGameData
from apps.lol.serializers import AggregatedStatsSerializer, \
    LeagueOfLegendsGameDataSerializer
from rest_framework import authentication, permissions
from apps.leaderboard.models import UserProfile


class LOLStatsById(generics.RetrieveAPIView):
    serializer_class = AggregatedStatsSerializer
    queryset = LOLAggregatedStats.objects.all()

class LOLAllStats(generics.ListAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LeagueOfLegendsGameDataSerializer

    def get_queryset(self):
        is_premium = UserProfile.objects.filter(user=self.request.user).first().is_premium()
        # Ordering by most recently added so that the user gets the most up to date stats first.
        data = LOLGameData.objects.filter(user_game_profile__user__user=self.request.user).order_by("-time_stamp")
        # Non-premium members only get the first result
        if data.first() is not None:
            if is_premium:
                return data.all()
            else:
                # Needs to return a list type
                return [data.first(), ]
        else:
            return None

# class LOLStatSummary(generics.)