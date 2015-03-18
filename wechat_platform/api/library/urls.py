# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^music/', include('api.library.music.urls', namespace='music')),
    url(r'^image/', include('api.library.image.urls', namespace='music')),
    url(r'^news/', include('api.library.news.urls', namespace='news')),
)