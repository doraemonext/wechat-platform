# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from api.library.image.views import LibraryImageListAPI, LibraryImageDetailAPI

urlpatterns = patterns('',
    url(r'^$', LibraryImageListAPI.as_view(), name='list'),
    url(r'^(?P<pk>[0-9]+)', LibraryImageDetailAPI.as_view(), name='detail'),
)