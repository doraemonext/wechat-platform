# -*- coding: utf-8 -*-

import logging

from django.core.exceptions import ObjectDoesNotExist

from system.plugin import PluginRuntimeError
from system.plugin.framework import PluginProcessorSystem
from system.library.text.models import LibraryText

logger_plugins = logging.getLogger(__name__)

__all__ = ['PluginSystemText']


class PluginSystemText(PluginProcessorSystem):
    """
    系统插件 - 文字消息
    """
    def process(self):
        try:
            content = LibraryText.objects.get(pk=self.reply_id)
        except ObjectDoesNotExist:
            logger_plugins.warning('No reply id %s found when get content from text library' % self.reply_id)
            raise PluginRuntimeError('No reply id %s found when get content from text library' % self.reply_id)

        return self.response_text(text=content.content)