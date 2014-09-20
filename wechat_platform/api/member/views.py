# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.urlresolvers import reverse

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, mixins
from rest_framework import status, parsers

from .serializer import MemberSerializer


class MemberListAPI(mixins.ListModelMixin, GenericAPIView):
    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    queryset = get_user_model().objects.all()
    serializer_class = MemberSerializer

    def get(self, request, *args, **kwargs):
        return super(MemberListAPI, self).list(request, *args, **kwargs)


class MemberDetailAPI(mixins.DestroyModelMixin, GenericAPIView):
    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    queryset = get_user_model().objects.all()
    serializer_class = MemberSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)