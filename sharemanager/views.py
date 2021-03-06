from django.shortcuts import render
from sharemanager.models import ShareManager, XPUser
from sharemanager.serializers import ShareManagerSerializer
from rest_framework import generics
from sharemanager.serializers import UserSerializer
from rest_framework import permissions
from sharemanager.permissions import IsOwnerOrReadOnly, IsSelf
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

from allauth.socialaccount import providers
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp
from allauth.socialaccount.providers.facebook.views import fb_complete_login
from allauth.socialaccount.helpers import complete_social_login
from sharemanager.auth import EverybodyCanAuthentication

from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from sendphoto import sendNotification


class ShareList(generics.ListCreateAPIView):
    queryset = ShareManager.objects.all()
    serializer_class = ShareManagerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    parser_classes = (MultiPartParser, FormParser,)
    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)
        sendNotification(instance)


class ShareDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShareManager.objects.all()
    serializer_class = ShareManagerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    authentication_classes = (SessionAuthentication, BasicAuthentication)

class UserList(generics.ListAPIView):
    queryset = XPUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    authentication_classes = (SessionAuthentication, BasicAuthentication)


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = XPUser.objects.all()
    serializer_class = UserSerializer
    #(permission for GET, permission for POST)
    permission_classes = (permissions.IsAuthenticated,IsSelf)
    authentication_classes = (SessionAuthentication, BasicAuthentication)

# Add a user to the system based on facebook token
class FacebookLoginOrSignup(APIView):   

    permission_classes = (AllowAny,)

    # this is a public api!!!
    authentication_classes = (EverybodyCanAuthentication,)

    def dispatch(self, *args, **kwargs):
        return super(FacebookLoginOrSignup, self).dispatch(*args, **kwargs)

    def post(self, request):
        data = JSONParser().parse(request)
        access_token = data.get('access_token', '')
        gcm_token = data.get('gcm_token', '')

        try:
            app = SocialApp.objects.get(provider="facebook")
            token = SocialToken(app=app, token=access_token)

            # check token against facebook
            login = fb_complete_login(request, app, token)
            login.token = token
            login.user.gcm_token = gcm_token
            login.state = SocialLogin.state_from_request(request)

            # add or update the user into users table
            ret = complete_social_login(request, login)

            # if we get here we've succeeded
            return Response(status=200, data={
                'success': True,
                'username': request.user.username,
                'user_id': request.user.pk,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            })

        except:
 
            return Response(status=401 ,data={
                'success': False,
                'reason': "Bad Access Token",
            })

