# -*- coding: utf-8 -*-

import logging

from django.core.exceptions import ObjectDoesNotExist

from system.plugin import PluginRuntimeError
from system.plugin.framework import PluginProcessorSystem
from system.library.news.models import LibraryNews

logger_plugins = logging.getLogger('plugins')

__all__ = ['PluginSystemNews']


class PluginSystemNews(PluginProcessorSystem):
    """
    系统插件 - 图文消息
    """
    def process(self):
        pattern = self.best_pattern(response_type='news')
        return self.response_news_library(pattern=pattern, library_id=self.reply_id)