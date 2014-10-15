# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from .views import GroupListAPI, GroupDetailAPI, PermissionListAPI


urlpatterns = patterns('',
    url(r'^$', GroupListAPI.as_view(), name='group_list'),
    url(r'^(?P<pk>[0-9]+)', GroupDetailAPI.as_view(), name='group_detail'),
    url(r'^permission/$', PermissionListAPI.as_view(), name='permission_list'),
)