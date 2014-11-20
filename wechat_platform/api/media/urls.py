# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from api.media.views import MediaDetailAPI, MediaUploadAPI


urlpatterns = patterns('',
    url(r'^$', MediaUploadAPI.as_view(), name='upload'),
    url(r'^(?P<pk>\w+)/$', MediaDetailAPI.as_view(), name='detail'),
)