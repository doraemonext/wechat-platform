# -*- coding: utf-8 -*-

from system.core.test import WechatTestCase
from system.rule.models import Rule
from system.keyword.models import Keyword


class KeywordTest(WechatTestCase):
    def test_keyword_search(self):
        rule_1 = Rule.manager.add(name='rule 1', reply_pattern=Rule.REPLY_PATTERN_RANDOM)
        rule_2 = Rule.manager.add(name='rule 2', reply_pattern=Rule.REPLY_PATTERN_ALL)
        rule_3 = Rule.manager.add(name='rule 3', reply_pattern=Rule.REPLY_PATTERN_FORWARD, status=False)
        rule_4 = Rule.manager.add(name='rule 4', reply_pattern=Rule.REPLY_PATTERN_REVERSE, top=True)

        # 测试包含匹配
        keyword_1 = Keyword.manager.add(rule=rule_1, keyword=u'你好', type=Keyword.TYPE_CONTAIN)
        keyword_2 = Keyword.manager.add(rule=rule_1, keyword=u'你', type=Keyword.TYPE_CONTAIN)
        keyword_3 = Keyword.manager.add(rule=rule_2, keyword=u'我们', type=Keyword.TYPE_CONTAIN)
        keyword_4 = Keyword.manager.add(rule=rule_2, keyword=u'我们有', type=Keyword.TYPE_CONTAIN)
        keyword_5 = Keyword.manager.add(rule=rule_3, keyword=u'deadline都快到了, 我竟然还在写测试 -_-# 真是少妇座的强迫症犯了……', status=False, type=Keyword.TYPE_CONTAIN)
        keyword_6 = Keyword.manager.add(rule=rule_4, keyword=u'你', type=Keyword.TYPE_CONTAIN)
        self.assertEqual(Keyword.manager.search(u'你好嘛'), keyword_6)
        self.assertEqual(Keyword.manager.search(u'我们'), keyword_3)
        self.assertEqual(Keyword.manager.search(u'你好'), keyword_6)
        self.assertEqual(Keyword.manager.search(u'你'), keyword_6)

        # 测试完全匹配
        keyword_7 = Keyword.manager.add(rule=rule_1, keyword=u'完全匹配测试', type=Keyword.TYPE_FULL)
        keyword_8 = Keyword.manager.add(rule=rule_2, keyword=u'完全', type=Keyword.TYPE_FULL)
        keyword_9 = Keyword.manager.add(rule=rule_3, keyword=u'完全匹配', type=Keyword.TYPE_FULL)
        self.assertEqual(Keyword.manager.search(u'完全'), keyword_8)
        self.assertEqual(Keyword.manager.search(u'完全匹配测试'), keyword_7)
        self.assertIsNone(Keyword.manager.search(u'完全匹配'))

        # 测试正则表达式匹配
        keyword_10 = Keyword.manager.add(rule=rule_1, keyword=u'^今天', type=Keyword.TYPE_REGEX)
        keyword_11 = Keyword.manager.add(rule=rule_2, keyword=u'^[^@]+@[^@]+\.[^@]{2,}$', type=Keyword.TYPE_REGEX)
        self.assertEqual(Keyword.manager.search(u'今天天气真好'), keyword_10)
        self.assertIsNone(Keyword.manager.search(u'天气预报说今天天气真好'))
        self.assertIsNone(Keyword.manager.search(u'doraemonext@xx'))
        self.assertEqual(Keyword.manager.search(u'doraemonext@gmail.com'), keyword_11)