# -*- coding: utf-8 -*-

import logging

from system.plugin.framework import PluginProcessorSystem

logger_plugins = logging.getLogger('plugins')

__all__ = ['PluginSystemImage']


class PluginSystemImage(PluginProcessorSystem):
    """
    系统插件 - 图片消息
    """
    def process(self):
        return self.response_image(library_id=self.reply_id)