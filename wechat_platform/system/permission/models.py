# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import Permission


class PermissionManager(models.Manager):
    def get(self):
        # 系统级权限需要排除在API之外
        exclude_value = [
            'add_permission',
            'change_permission',
            'delete_permission',
            'add_contenttype',
            'change_contenttype',
            'delete_contenttype',
            'add_session',
            'change_session',
            'delete_session',
        ]

        queryset = super(PermissionManager, self).get_queryset()
        for codename in exclude_value:
            queryset = queryset.exclude(codename=codename)
        return queryset


class CustomPermission(Permission):
    objects = models.Manager()
    manager = PermissionManager()

    class Meta:
        proxy = True
