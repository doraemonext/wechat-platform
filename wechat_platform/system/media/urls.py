# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

from system.media.views import download


urlpatterns = patterns('',
    url(r'^(?P<key>\w+)/$', download, name="download"),
)