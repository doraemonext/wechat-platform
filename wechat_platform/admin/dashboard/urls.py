# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from .views import DashboardView


urlpatterns = patterns('',
    url(r'^$', DashboardView.as_view(), name='dashboard'),
)