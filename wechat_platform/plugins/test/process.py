# -*- coding: utf-8 -*-

import logging

from system.plugin.framework import PluginProcessor

logger_plugins = logging.getLogger('plugins')

__all__ = ['PluginTest']


class PluginTest(PluginProcessor):
    """
    测试插件
    """
    def process(self):
        return self.response_text_basic(text='你好')