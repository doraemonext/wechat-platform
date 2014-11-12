# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^music/', include('api.library.music.urls', namespace='music')),
)