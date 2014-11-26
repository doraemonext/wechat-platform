# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from api.library.news.views import LibraryNewsListAPI

urlpatterns = patterns('',
    url(r'^$', LibraryNewsListAPI.as_view(), name='list'),
#    url(r'^(?P<pk>[0-9]+)', LibraryMusicDetailAPI.as_view(), name='detail'),
)