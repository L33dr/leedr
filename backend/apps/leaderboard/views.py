"""
Base views for the leaderboard application. Used primarily for user based views.
"""
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.twitch.views import TwitchOAuth2Adapter
from rest_auth.registration.views import SocialLogin
from rest_framework import generics, status
from django.views.generic import View
from django.http import HttpResponse
from django.views.generic.edit import FormView
from rest_framework.response import Response
from rest_framework.views import APIView
from forms import SignupForm
from models import GameDetail, UserProfile, UserGameProfile
from rest_framework import authentication, permissions
from serializers import GameDetailSerializer, UserProfileSerializer, UserGameProfileSerializer, CommentSerializer
from apps.leaderboard.tasks import send_contact_request_alert_task, send_contact_request_reply_task
from apps.lol.tasks import get_id_then_update_stats

class FacebookLogin(SocialLogin):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLogin):
    adapter_class = GoogleOAuth2Adapter


class TwitchLogin(SocialLogin):
    adapter_class = TwitchOAuth2Adapter


class VerifyEmail(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<script>(function () {window.location.href = "http://localhost:8000/app/#/confirm-email/'
                            + kwargs['key'] + '"})();</script>')

class GoogleCallBack(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<script>(function () {window.location.href = "http://localhost:8000/app/#/googleCallback/'
                            + kwargs['key'] + '"})();</script>')

class SignupView(FormView):
    form_class = SignupForm


class GameListView(generics.ListAPIView):
    serializer_class = GameDetailSerializer
    queryset = GameDetail.objects.all()


class UserProfileView(generics.ListAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user).all()

class UserProfileUpdateView(generics.UpdateAPIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

class UserGameProfileView(generics.ListCreateAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserGameProfileSerializer

    def get_queryset(self):
        return UserGameProfile.objects.filter(user=self.request.user).all()

    def post(self, request, *args, **kwargs):
        user = UserProfile.objects.get(user=self.request.user)
        game = GameDetail.objects.filter(shorthand_name=request.data['game']['shorthand_name']).first()
        serializer = UserGameProfileSerializer(data=request.data)
        if serializer.is_valid():
            try:
                profile = serializer.create(serializer.validated_data, user=user, game=game)
                get_id_then_update_stats.delay(request.data['game_user_name'], request.data['region'], profile)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValueError:
                return Response("You cannot add the same game profile twice!", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Comment(APIView):
    def post(self, request, format=None):
        x_forward = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forward:
            request.data['ip_address'] = x_forward.split(',')[-1].strip()
        else:
            request.data['ip_address'] = request.META.get('REMOTE_ADDR')
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            send_contact_request_reply_task.delay(request.data['name'], request.data['email'])
            send_contact_request_alert_task.delay(request.data['name'], request.data['email'], request.data['comment'],
                       request.data['ip_address'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
