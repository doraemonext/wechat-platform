# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from .views import OfficialAccountListAPI, OfficialAccountDetailAPI, OfficialAccountSwitchAPI


urlpatterns = patterns('',
    url(r'^$', OfficialAccountListAPI.as_view(), name='official_account_list'),
    url(r'^(?P<pk>[0-9]+)', OfficialAccountDetailAPI.as_view(), name='official_account_detail'),
    url(r'^switch/', OfficialAccountSwitchAPI.as_view(), name='official_account_switch'),
)