# -*- coding: utf-8 -*-

import json
from StringIO import StringIO

from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.http import Http404

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, mixins, filters
from rest_framework import status, parsers
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from system.library.news.models import LibraryNews
from system.library.news.exceptions import LibraryNewsException
from system.official_account.models import OfficialAccount
from api.library.news.serializers import LibraryNewsSingleCreate, LibraryNewsCreate
from api.library.news.serializers import LibraryNewsListSeriailzer, LibraryNewsDetailSerializer, LibraryNewsSingleCreateSerializer, LibraryNewsCreateSerializer


class LibraryNewsListAPI(mixins.ListModelMixin, GenericAPIView):
    """
    系统素材库 - 图文素材 (列表View, 仅限GET/POST)

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
        try:
            serializer = LibraryNewsCreateSerializer(data={
                'official_account': request.DATA.get('official_account'),
                'news_array': json.loads(request.DATA.get('news_array')),
            })
        except ValueError:
            return Response({'news_array': [u'内容非法']}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LibraryNewsDetailAPI(mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    """
    系统素材库 - 图文素材 (单个对象View, 仅限GET/PUT/DELETE)
    """
    permission_classes = (permissions.IsAuthenticated, )
    model = LibraryNews
    serializer_class = LibraryNewsDetailSerializer

    def get(self, request, *args, **kwargs):
        obj = self.get_object_or_none()
        if not obj or obj.parent:  # 仅允许获得多图文的首图文ID
            raise Http404()

        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        obj = self.get_object_or_none()
        if not obj or obj.parent:  # 仅允许更新, 对于新建或非首图文ID直接禁止
            raise Http404()

        try:
            serializer = LibraryNewsCreateSerializer(data={
                'news_id': obj.pk,
                'official_account': request.DATA.get('official_account'),
                'news_array': json.loads(request.DATA.get('news_array')),
            })
        except ValueError:
            return Response({'news_array': [u'内容非法']}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        return super(LibraryNewsDetailAPI, self).destroy(request, *args, **kwargs)


class LibraryNewsSyncAPI(mixins.UpdateModelMixin, GenericAPIView):
    """
    系统素材库 - 图文素材同步 API (仅限 PUT)
    """
    permission_classes = (permissions.IsAuthenticated, )
    model = LibraryNews

    def put(self, request, *args, **kwargs):
        obj = self.get_object_or_none()
        if not obj or obj.parent:  # 仅允许更新, 对于新建或非首图文ID直接禁止
            raise Http404()
        try:
            news = LibraryNews.manager.get(
                official_account=obj.official_account,
                plugin_iden=obj.plugin_iden,
                root=obj
            )
        except LibraryNews.DoesNotExist, e:
            raise Http404()

        try:
            msgid = LibraryNews.manager.sync(official_account=obj.official_account, news=news)
        except LibraryNewsException:
            return Response({'non_field_errors': [u'同步到微信官方服务器时发生错误']}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'msgid': msgid}, status=status.HTTP_200_OK)