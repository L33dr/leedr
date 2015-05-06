"""
Base views for the leaderboard application. Used primarily for user based views.
"""
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.twitch.views import TwitchOAuth2Adapter
from rest_framework.response import Response
from rest_auth.registration.views import SocialLogin
from rest_framework import generics
from django.views.generic import View
from django.http import HttpResponse
from django.views.generic.edit import FormView
from forms import SignupForm
from models import GameDetail, UserProfile, UserGameProfile
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework.views import APIView
from serializers import GameDetailSerializer, UserProfileSerializer, UserGameProfileSerializer


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
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


class UserGameProfileView(generics.ListAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserGameProfileSerializer

    def get_queryset(self):
        return UserGameProfile.objects.filter(user__user__username__exact=self.request.user).all()
