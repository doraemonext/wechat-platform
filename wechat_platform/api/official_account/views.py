# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, mixins
from rest_framework import status, parsers

from system.official_account.models import OfficialAccount
from .serializer import OfficialAccountSerializer


class OfficialAccountListAPI(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    model = OfficialAccount
    serializer_class = OfficialAccountSerializer

    def get(self, request, *args, **kwargs):
        return super(OfficialAccountListAPI, self).list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(OfficialAccountListAPI, self).create(request, *args, **kwargs)


class OfficialAccountDetailAPI(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    model = OfficialAccount
    serializer_class = OfficialAccountSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)