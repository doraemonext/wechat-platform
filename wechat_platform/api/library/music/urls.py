# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from api.library.music.views import LibraryMusicListAPI, LibraryMusicDetailAPI

urlpatterns = patterns('',
    url(r'^$', LibraryMusicListAPI.as_view(), name='list'),
    url(r'^(?P<pk>[0-9]+)', LibraryMusicDetailAPI.as_view(), name='detail'),
)