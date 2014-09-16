# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from .views import LoginAPI


urlpatterns = patterns('',
    url(r'^login/$', LoginAPI.as_view(), name='login'),
)