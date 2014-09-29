# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from .views import ListenView


urlpatterns = patterns('',
    url(r'^$', ListenView.as_view(), name="index"),
)