# -*- coding: utf-8 -*-

import logging

from django.core.exceptions import ObjectDoesNotExist

from system.plugin import PluginRuntimeError
from system.plugin.framework import PluginProcessorSystem
from system.library.text.models import LibraryText

logger_plugin = logging.getLogger(__name__)

__all__ = ['PluginSystemText']


class PluginSystemText(PluginProcessorSystem):
    """
    系统插件 - 文字消息
    """
    def process(self):
        try:
            content = LibraryText.objects.get(pk=self.reply_id)
        except ObjectDoesNotExist:
            logger_plugin.warning('No reply id found when get content from text library [ReplyID] %s' % self.reply_id)
            raise PluginRuntimeError('No reply id found when get content from text library')

        return self.response_text(text=content)