# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, mixins, filters
from rest_framework import status, parsers

from system.library.news.models import LibraryNews
from api.library.news.serializers import LibraryNewsListSeriailzer


class LibraryNewsListAPI(mixins.ListModelMixin, GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    model = LibraryNews
    serializer_class = LibraryNewsListSeriailzer
    # filter_fields = ('official_account', 'plugin_iden', 'title', 'description')
    # search_fields = ('title', 'description')
    # ordering = ('id', )

    def get_queryset(self):
        return LibraryNews.manager.get_list(official_account=self.request.GET.get('official_account'))

    def get(self, request, *args, **kwargs):
        if not request.GET.get('official_account'):
            return Response('not found')

        return super(LibraryNewsListAPI, self).list(request, *args, **kwargs)