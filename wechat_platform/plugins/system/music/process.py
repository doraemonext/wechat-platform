# -*- coding: utf-8 -*-

import logging

from django.core.exceptions import ObjectDoesNotExist

from system.plugin import PluginRuntimeError
from system.plugin.framework import PluginProcessorSystem
from system.library.music.models import LibraryMusic

logger_plugins = logging.getLogger(__name__)

__all__ = ['PluginSystemMusic']


class PluginSystemMusic(PluginProcessorSystem):
    """
    系统插件 - 音乐消息
    """
    def process(self):
        return self.response_music_library(library_id=self.reply_id)