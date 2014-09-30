# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from .views import GroupListAPI, GroupDetailAPI


urlpatterns = patterns('',
    url(r'^$', GroupListAPI.as_view(), name='group_list'),
    url(r'^(?P<pk>[0-9]+)', GroupDetailAPI.as_view(), name='group_detail'),
)