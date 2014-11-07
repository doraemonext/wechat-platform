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
        try:
            music = LibraryMusic.objects.get(pk=self.reply_id)
        except ObjectDoesNotExist:
            logger_plugins.warning('No reply id %s found when get content from music library' % self.reply_id)
            raise PluginRuntimeError('No reply id %s found when get content from music library' % self.reply_id)

        return self.response_music(
            music_url=music.music_url,
            title=music.title,
            description=music.description,
            hq_music_url=music.hq_music_url,
            thumb_media_id=music.thumb_media_id,
        )