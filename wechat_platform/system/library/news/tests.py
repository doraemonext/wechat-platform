# -*- coding: utf-8 -*-

from system.core.test import WechatTestCase
from system.official_account.models import OfficialAccount
from system.library.news.models import LibraryNews


class LibraryNewsTest(WechatTestCase):
    def test_news_remote(self):
        official_account = self.make_official_account(level=OfficialAccount.LEVEL_1)
        news_dict = [
            {
                'title': 'title1',
                'description': 'description1',
                'picurl': 'http://www.baidu.com/',
                'url': 'http://www.baidu.com/',
            },
            {
                'title': 'title2',
                'description': 'description2',
                'url': 'http://www.google.com',
            },
            {
                'title': 'title3',
                'picurl': 'http://www.baidu.com/',
                'url': 'http://www.google.com',
            }
        ]

        news = LibraryNews.manager.add_remote(official_account=official_account, plugin_iden='news', news=news_dict)
        result = LibraryNews.manager.get(official_account=official_account, plugin_iden='news', root=news)
        self.assertEqual(3, len(result))
        tmp = LibraryNews.objects.filter(official_account=official_account).filter(plugin_iden='news').filter(parent=None)[0]
        self.assertEqual(tmp.title, 'title1')
        self.assertEqual(tmp.description, 'description1')
        self.assertEqual(tmp.picurl, 'http://www.baidu.com/')
        self.assertEqual(tmp.url, 'http://www.baidu.com/')
        self.assertEqual(result[0], tmp)
        tmp = LibraryNews.objects.filter(official_account=official_account).filter(plugin_iden='news').filter(parent=tmp)[0]
        self.assertEqual(tmp.title, 'title2')
        self.assertEqual(tmp.description, 'description2')
        self.assertEqual(tmp.picurl, None)
        self.assertEqual(tmp.url, 'http://www.google.com')
        self.assertEqual(result[1], tmp)
        tmp = LibraryNews.objects.filter(official_account=official_account).filter(plugin_iden='news').filter(parent=tmp)[0]
        self.assertEqual(tmp.title, 'title3')
        self.assertEqual(tmp.description, None)
        self.assertEqual(tmp.picurl, 'http://www.baidu.com/')
        self.assertEqual(tmp.url, 'http://www.google.com')
        self.assertEqual(result[2], tmp)