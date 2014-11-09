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
        except ObjectDoesNotExist:
            logger_plugins.warning('No reply id %s found when get content from news library' % self.reply_id)
            raise PluginRuntimeError('No reply id %s found when get content from news library' % self.reply_id)

        pattern = self.best_pattern(response_type='news')
        news_dealt = []
        news_instances = LibraryNews.manager.get(official_account=root.official_account, root=root)
        if pattern == 'basic':
            for news in news_instances:
                news_dealt.append({
                    'title': news.title,
                    'description': news.description,
                    'picurl': news.picurl,
                    'url': news.url,
                })
            return self.response_news(pattern=pattern, news=news_dealt)
        elif pattern == 'service':
            pass
        else:
            if news_instances[0].msgid:
                return self.response_news(pattern=pattern, msgid=news_instances[0].msgid)
            else:
                for news in news_instances:
                    news_dealt.append({
                        'title': news.title,
                        'author': news.author,
                        'summary': news.description,
                        'content': news.content,
                        'picture_id': news.picture_id,
                        'picture': news.picture,
                        'picurl': news.picurl,
                        'from_url': news.from_url,
                    })
                return self.response_news(pattern=pattern, news=news_dealt)