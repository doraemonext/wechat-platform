# -*- coding: utf-8 -*-

import logging

from system.plugin.framework import PluginProcessorSystem

logger_plugins = logging.getLogger(__name__)

__all__ = ['PluginSystemText']


class PluginSystemText(PluginProcessorSystem):
    """
    系统插件 - 文字消息
    """
    def process(self):
        return self.response_text_library(library_id=self.reply_id)