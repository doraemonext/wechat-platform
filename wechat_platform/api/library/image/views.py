# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, mixins, filters
from rest_framework import status, parsers

from system.official_account.models import OfficialAccount
from system.library.image.models import LibraryImage
from api.library.image.serializer import LibraryImageSerializer


class LibraryImageListAPI(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    model = LibraryImage
    serializer_class = LibraryImageSerializer
    filter_fields = ('official_account', 'plugin_iden')
    ordering = ('id', )

    def get_queryset(self):
        return LibraryImage.manager.get_list(official_account=self.request.GET.get('official_account'))

    def get(self, request, *args, **kwargs):
        # 对 official_account 参数进行检查
        official_account_id = request.GET.get('official_account')
        if not official_account_id:
            return Response({'official_account': [u'缺少 official_account 参数']}, status=status.HTTP_400_BAD_REQUEST)
        if not OfficialAccount.manager.exists(official_account_id):
            return Response({'official_account': [u'指定公众号不存在']}, status=status.HTTP_400_BAD_REQUEST)

        return super(LibraryImageListAPI, self).list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(LibraryImageListAPI, self).create(request, *args, **kwargs)


class LibraryImageDetailAPI(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    model = LibraryImage
    serializer_class = LibraryImageSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)