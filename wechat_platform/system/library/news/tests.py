# -*- coding: utf-8 -*-

from system.core.test import WechatTestCase
from system.official_account.models import OfficialAccount
from system.library.news.models import LibraryNews
from system.rule.models import Rule
from system.rule_match.models import RuleMatch


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

    def test_news_modify(self):
        official_account = self.make_official_account(level=OfficialAccount.LEVEL_1)
        news_dict_1 = [
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
        news_dict_2 = [
            {
                'title': 'title4',
                'description': 'description4',
                'picurl': 'http://www.baidu.com/',
                'url': 'http://www.baidu.com/',
            },
            {
                'title': 'title5',
                'description': 'description5',
                'url': 'http://www.google.com',
            }
        ]

        LibraryNews.objects.all().delete()
        RuleMatch.objects.all().delete()
        news_1 = LibraryNews.manager.add_mix(official_account=official_account, plugin_iden='news', news=news_dict_1)
        news_2 = LibraryNews.manager.add_mix(official_account=official_account, plugin_iden='news', news=news_dict_2)
        rule = Rule.manager.add(official_account=official_account, name=u'测试规则', reply_pattern=Rule.REPLY_PATTERN_ALL)
        rule_match_1 = RuleMatch.manager.add(rule=rule, plugin_iden='news', reply_id=news_1.pk)
        rule_match_2 = RuleMatch.manager.add(rule=rule, plugin_iden='news', reply_id=news_2.pk)
        self.assertEqual(5, LibraryNews.objects.count())  # 共创建了6条记录
        self.assertEqual(2, RuleMatch.objects.count())
        new_news = LibraryNews.manager.modify(pk=news_1.pk, news=news_dict_2)
        self.assertEqual(4, LibraryNews.objects.count())
        new_rule_match = RuleMatch.manager.get(rule=rule).filter(reply_id=new_news.pk)
        self.assertEqual(1, new_rule_match.count())
        origin_rule_match = RuleMatch.manager.get(rule=rule).filter(reply_id=news_1.pk)
        self.assertEqual(0, origin_rule_match.count())
