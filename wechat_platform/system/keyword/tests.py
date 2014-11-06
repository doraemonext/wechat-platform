# -*- coding: utf-8 -*-

from system.core.test import WechatTestCase
from system.official_account.models import OfficialAccount
from system.rule.models import Rule
from system.keyword.models import Keyword


class KeywordTest(WechatTestCase):
    def test_add_keyword(self):
        """
        测试添加关键字
        """
        official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_3, name='name', email='email@email.com', original='original', wechat='wechat')

        rule = Rule.manager.add(official_account=official_account, name='rule test', reply_pattern=Rule.REPLY_PATTERN_ALL)
        keyword = Keyword.manager.add(rule, keyword='keyword')
        self.assertEqual(keyword.rule, rule)
        self.assertEqual(keyword.keyword, 'keyword')
        self.assertEqual(keyword.status, True)
        self.assertEqual(keyword.type, Keyword.TYPE_FULL)

    def test_keyword_search(self):
        """
        测试关键字搜索
        """
        official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_3, name='name', email='email@email.com', original='original', wechat='wechat')

        rule_1 = Rule.manager.add(official_account=official_account, name='rule 1', reply_pattern=Rule.REPLY_PATTERN_RANDOM)
        rule_2 = Rule.manager.add(official_account=official_account, name='rule 2', reply_pattern=Rule.REPLY_PATTERN_ALL)
        rule_3 = Rule.manager.add(official_account=official_account, name='rule 3', reply_pattern=Rule.REPLY_PATTERN_FORWARD, status=False)
        rule_4 = Rule.manager.add(official_account=official_account, name='rule 4', reply_pattern=Rule.REPLY_PATTERN_REVERSE, top=True)

        # 测试包含匹配
        keyword_1 = Keyword.manager.add(rule=rule_1, keyword=u'你好', type=Keyword.TYPE_CONTAIN)
        keyword_2 = Keyword.manager.add(rule=rule_1, keyword=u'你', type=Keyword.TYPE_CONTAIN)
        keyword_3 = Keyword.manager.add(rule=rule_2, keyword=u'我们', type=Keyword.TYPE_CONTAIN)
        keyword_4 = Keyword.manager.add(rule=rule_2, keyword=u'我们有', type=Keyword.TYPE_CONTAIN)
        keyword_5 = Keyword.manager.add(rule=rule_3, keyword=u'deadline都快到了, 我竟然还在写测试 -_-# 真是少妇座的强迫症犯了……', status=False, type=Keyword.TYPE_CONTAIN)
        keyword_6 = Keyword.manager.add(rule=rule_4, keyword=u'你', type=Keyword.TYPE_CONTAIN)
        self.assertEqual(Keyword.manager.search(official_account=official_account, keyword=u'你好嘛'), keyword_6)
        self.assertEqual(Keyword.manager.search(official_account=official_account, keyword=u'我们'), keyword_3)
        self.assertEqual(Keyword.manager.search(official_account=official_account, keyword=u'你好'), keyword_6)
        self.assertEqual(Keyword.manager.search(official_account=official_account, keyword=u'你'), keyword_6)

        # 测试完全匹配
        keyword_7 = Keyword.manager.add(rule=rule_1, keyword=u'完全匹配测试', type=Keyword.TYPE_FULL)
        keyword_8 = Keyword.manager.add(rule=rule_2, keyword=u'完全', type=Keyword.TYPE_FULL)
        keyword_9 = Keyword.manager.add(rule=rule_3, keyword=u'完全匹配', type=Keyword.TYPE_FULL)
        self.assertEqual(Keyword.manager.search(official_account=official_account, keyword=u'完全'), keyword_8)
        self.assertEqual(Keyword.manager.search(official_account=official_account, keyword=u'完全匹配测试'), keyword_7)
        self.assertIsNone(Keyword.manager.search(official_account=official_account, keyword=u'完全匹配'))

        # 测试正则表达式匹配
        keyword_10 = Keyword.manager.add(rule=rule_1, keyword=u'^今天', type=Keyword.TYPE_REGEX)
        keyword_11 = Keyword.manager.add(rule=rule_2, keyword=u'^[^@]+@[^@]+\.[^@]{2,}$', type=Keyword.TYPE_REGEX)
        self.assertEqual(Keyword.manager.search(official_account=official_account, keyword=u'今天天气真好'), keyword_10)
        self.assertIsNone(Keyword.manager.search(official_account=official_account, keyword=u'天气预报说今天天气真好'))
        self.assertIsNone(Keyword.manager.search(official_account=official_account, keyword=u'doraemonext@xx'))
        self.assertEqual(Keyword.manager.search(official_account=official_account, keyword=u'doraemonext@gmail.com'), keyword_11)