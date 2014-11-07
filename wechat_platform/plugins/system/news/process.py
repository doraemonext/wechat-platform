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
        try:
            root = LibraryNews.objects.get(pk=self.reply_id)
            news_instances = [root] + LibraryNews.manager.get(official_account=root.official_account, root=root)
            news_list = []
            for news in news_instances:
                news_list.append({
                    'title': news.title,
                    'description': news.description,
                    'picurl': news.picurl,
                    'url': news.url,
                })
            logger_plugins.debug(news_instances)
        except ObjectDoesNotExist:
            logger_plugins.warning('No reply id %s found when get content from news library' % self.reply_id)
            raise PluginRuntimeError('No reply id %s found when get content from news library' % self.reply_id)

        return self.response_news(news=news_list)