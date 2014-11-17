# -*- coding: utf-8 -*-

import os

import magic
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist

from system.media.models import Media


def download(request, key):
    try:
        media = Media.manager.get(key=key)
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('File not found')

    return HttpResponse(media.media.file, content_type=magic.from_buffer(media.media.file.read(), mime=True))
