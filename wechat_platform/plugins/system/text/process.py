# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist

from system.core.exceptions import PluginRuntimeError
from system.plugin.framework import PluginProcessorSystem
from system.library.text.models import LibraryText

__all__ = ['PluginSystemText']


class PluginSystemText(PluginProcessorSystem):
    """
    系统插件 - 文字消息
    """
    def process(self):
        try:
            content = LibraryText.objects.get(pk=self.reply_id)
        except ObjectDoesNotExist:
            raise PluginRuntimeError('no reply id found when get content from text library')

        return self.response_text(text=content)