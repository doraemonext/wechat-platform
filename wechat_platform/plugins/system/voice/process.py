# -*- coding: utf-8 -*-

import logging

from system.plugin.framework import PluginProcessorSystem

logger_plugins = logging.getLogger('plugins')

__all__ = ['PluginSystemVoice']


class PluginSystemVoice(PluginProcessorSystem):
    """
    系统插件 - 语音消息
    """
    def process(self):
        return self.response_voice(library_id=self.reply_id)