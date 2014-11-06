# -*- coding: utf-8 -*-

from system.core.test import WechatTestCase
from system.official_account.models import OfficialAccount
from system.rule.models import Rule


class RuleTest(WechatTestCase):
    def test_add_rule_with_default_value(self):
        official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_3, name='name', email='email@email.com', original='original', wechat='wechat')

        rule = Rule.manager.add(official_account=official_account, name=u'测试规则', reply_pattern=Rule.REPLY_PATTERN_ALL)
        self.assertEqual(rule.name, u'测试规则')
        self.assertEqual(rule.reply_pattern, Rule.REPLY_PATTERN_ALL)
        self.assertTrue(rule.status)
        self.assertFalse(rule.top)
        self.assertEqual(0, rule.order)

    def test_add_rule(self):
        official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_3, name='name', email='email@email.com', original='original', wechat='wechat')

        rule = Rule.manager.add(official_account=official_account, name=u'测试规则', reply_pattern=Rule.REPLY_PATTERN_ALL, status=False, top=True, order=100)
        self.assertEqual(rule.name, u'测试规则')
        self.assertEqual(rule.reply_pattern, Rule.REPLY_PATTERN_ALL)
        self.assertFalse(rule.status)
        self.assertTrue(rule.top)
        self.assertEqual(100, rule.order)