# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, mixins
from rest_framework import status, parsers

from system.media.models import Media
from api.media.serializer import MediaSerializer, MediaUploadSerializer


class MediaDetailAPI(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    model = Media
    serializer_class = MediaSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class MediaUploadAPI(mixins.CreateModelMixin, GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    model = Media
    serializer_class = MediaUploadSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
