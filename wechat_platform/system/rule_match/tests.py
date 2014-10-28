# -*- coding: utf-8 -*-

from system.core.test import WechatTestCase
from system.rule.models import Rule
from system.rule_match.models import RuleMatch


class RuleResponseTest(WechatTestCase):
    def test_add_rule_response(self):
        """
        测试添加新的规则响应
        """
        self.assertEqual(0, RuleMatch.objects.count())
        rule = Rule.manager.add(name='rule one', reply_pattern=Rule.REPLY_PATTERN_ALL)
        rule_match = RuleMatch.manager.add(rule=rule, plugin_iden='text', order=5, status=False)
        self.assertEqual(1, RuleMatch.objects.count())
        self.assertEqual(rule_match.rule, rule)
        self.assertEqual(rule_match.plugin_iden, 'text')
        self.assertEqual(rule_match.order, 5)
        self.assertFalse(rule_match.status)