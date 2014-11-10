# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from system.library.news.views import NewsDetailView


urlpatterns = patterns('',
    url(r'^(?P<pk>[0-9]+)/', NewsDetailView.as_view(), name='detail'),
)