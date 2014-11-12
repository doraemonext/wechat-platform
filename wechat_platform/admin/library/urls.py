# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^music/', include('admin.library.music.urls', namespace='music')),
)