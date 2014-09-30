# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group

from rest_framework.generics import GenericAPIView
from rest_framework import authentication, permissions, mixins

from .serializer import GroupSerializer


class GroupListAPI(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    model = Group
    serializer_class = GroupSerializer

    def filter_queryset(self, queryset):
        """ 将用户组结果按ID排序 """
        queryset = super(GroupListAPI, self).filter_queryset(queryset)
        queryset = queryset.order_by('id')
        return queryset

    def get(self, request, *args, **kwargs):
        return super(GroupListAPI, self).list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(GroupListAPI, self).create(request, *args, **kwargs)


class GroupDetailAPI(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    authentication_classes = (authentication.SessionAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    model = Group
    serializer_class = GroupSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)