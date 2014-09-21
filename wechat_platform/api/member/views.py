# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, mixins
from rest_framework import status, parsers

from .serializer import MemberSerializer, GroupSerializer


class MemberListAPI(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    queryset = get_user_model().objects.all()
    serializer_class = MemberSerializer

    def get(self, request, *args, **kwargs):
        return super(MemberListAPI, self).list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(MemberListAPI, self).create(request, *args, **kwargs)

    def post_save(self, obj, created=False):
        pass


class MemberDetailAPI(mixins.DestroyModelMixin, GenericAPIView):
    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    model = get_user_model()
    serializer_class = MemberSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class GroupListAPI(mixins.ListModelMixin, GenericAPIView):
    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    model = Group
    serializer_class = GroupSerializer

    def get(self, request, *args, **kwargs):
        return super(GroupListAPI, self).list(request, *args, **kwargs)