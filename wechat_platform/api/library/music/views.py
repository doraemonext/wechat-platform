# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, mixins
from rest_framework import status, parsers

from system.library.music.models import LibraryMusic
from api.library.music.serializer import LibraryMusicSerializer


class LibraryMusicListAPI(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    model = LibraryMusic
    serializer_class = LibraryMusicSerializer

    def get(self, request, *args, **kwargs):
        return super(LibraryMusicListAPI, self).list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(LibraryMusicListAPI, self).create(request, *args, **kwargs)


class LibraryMusicDetailAPI(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    model = LibraryMusic
    serializer_class = LibraryMusicSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)