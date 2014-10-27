# -*- coding: utf-8 -*-

from system.core.test import WechatTestCase
from system.rule.models import Rule


class RuleTest(WechatTestCase):
    def test_add_rule_with_default_value(self):
        self.assertEqual(0, Rule.objects.count())
        rule = Rule.manager.add(name=u'测试规则', reply_pattern=Rule.REPLY_PATTERN_ALL)
        self.assertEqual(1, Rule.objects.count())
        self.assertEqual(rule.name, u'测试规则')
        self.assertEqual(rule.reply_pattern, Rule.REPLY_PATTERN_ALL)
        self.assertTrue(rule.status)
        self.assertFalse(rule.top)
        self.assertEqual(0, rule.order)

    def test_add_rule(self):
        self.assertEqual(0, Rule.objects.count())
        rule = Rule.manager.add(name=u'测试规则', reply_pattern=Rule.REPLY_PATTERN_ALL, status=False, top=True, order=100)
        self.assertEqual(1, Rule.objects.count())
        self.assertEqual(rule.name, u'测试规则')
        self.assertEqual(rule.reply_pattern, Rule.REPLY_PATTERN_ALL)
        self.assertFalse(rule.status)
        self.assertTrue(rule.top)
        self.assertEqual(100, rule.order)