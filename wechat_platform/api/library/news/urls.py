# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from api.library.news.views import LibraryNewsListAPI, LibraryNewsDetailAPI

urlpatterns = patterns('',
    url(r'^$', LibraryNewsListAPI.as_view(), name='list'),
    url(r'^(?P<pk>[0-9]+)', LibraryNewsDetailAPI.as_view(), name='detail'),
)