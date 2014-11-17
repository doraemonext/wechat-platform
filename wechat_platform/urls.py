# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name="home"),
    url(r'^admin/', include('admin.urls', namespace='admin')),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^listen/', include('system.listen.urls', namespace='listen')),
    url(r'^news/', include('system.library.news.urls', namespace='news')),
    url(r'^filetranslator/', include('system.media.urls', namespace='filetranslator')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)