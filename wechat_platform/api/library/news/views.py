# -*- coding: utf-8 -*-

import json
from StringIO import StringIO

from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, mixins, filters
from rest_framework import status, parsers
from rest_framework.parsers import JSONParser

from system.library.news.models import LibraryNews
from system.official_account.models import OfficialAccount
from api.library.news.serializers import LibraryNewsSingleCreate, LibraryNewsCreate
from api.library.news.serializers import LibraryNewsListSeriailzer, LibraryNewsSingleCreateSerializer, LibraryNewsCreateSerializer


class LibraryNewsListAPI(mixins.ListModelMixin, GenericAPIView):
    """
    系统素材库 - 图文素材 (列表View, 仅限GET)

    注意请求中必须提供 official_account 参数
    """
    permission_classes = (permissions.IsAuthenticated, )
    model = LibraryNews
    serializer_class = LibraryNewsListSeriailzer
    filter_fields = ('official_account', 'plugin_iden', 'title', 'description', 'author')
    search_fields = ('title', 'description', 'author')
    ordering = ('-datetime', )

    def get_queryset(self):
        return LibraryNews.manager.get_list(official_account=self.request.GET.get('official_account'))

    def get(self, request, *args, **kwargs):
        """
        获取图文素材列表
        """
        # 对 official_account 参数进行检查
        official_account_id = request.GET.get('official_account')
        if not official_account_id:
            return Response({'official_account': [u'缺少 official_account 参数']}, status=status.HTTP_400_BAD_REQUEST)
        if not OfficialAccount.manager.exists(official_account_id):
            return Response({'official_account': [u'指定公众号不存在']}, status=status.HTTP_400_BAD_REQUEST)

        return super(LibraryNewsListAPI, self).list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        新建图文素材
        """
        serializer = LibraryNewsCreateSerializer(data={
            'official_account': request.DATA.get('official_account'),
            'news_array': json.loads(request.DATA.get('news_array')),
        })

        if serializer.is_valid():
            serializer.save(force_insert=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)