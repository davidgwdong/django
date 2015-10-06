from django.shortcuts import render
from sharemanager.models import ShareManager
from sharemanager.serializers import ShareManagerSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from sharemanager.serializers import UserSerializer
from rest_framework import permissions
from sharemanager.permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class ShareList(generics.ListCreateAPIView):
    queryset = ShareManager.objects.all()
    serializer_class = ShareManagerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ShareDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShareManager.objects.all()
    serializer_class = ShareManagerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    authentication_classes = (SessionAuthentication, BasicAuthentication)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

