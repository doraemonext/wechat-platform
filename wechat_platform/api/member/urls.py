# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from .views import MemberListAPI, MemberDetailAPI


urlpatterns = patterns('',
    url(r'^$', MemberListAPI.as_view(), name='member_list'),
    url(r'(?P<pk>[0-9]+)', MemberDetailAPI.as_view(), name='member_detail'),
)