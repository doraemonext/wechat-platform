# -*- coding: utf-8 -*-

from system.core.test import WechatTestCase
from system.official_account.models import OfficialAccount
from system.rule.models import Rule
from system.rule_match.models import RuleMatch


class RuleMatchTest(WechatTestCase):
    def test_add_rule_match(self):
        """
        测试添加新的规则匹配
        """
        official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_3, name='name', email='email@email.com', original='original', wechat='wechat')

        rule = Rule.manager.add(official_account=official_account, name='rule one', reply_pattern=Rule.REPLY_PATTERN_ALL)
        rule_match = RuleMatch.manager.add(rule=rule, plugin_iden='text', order=5, status=False)
        self.assertEqual(rule_match.rule, rule)
        self.assertEqual(rule_match.plugin_iden, 'text')
        self.assertEqual(rule_match.order, 5)
        self.assertFalse(rule_match.status)

    def test_get_rule_match(self):
        """
        测试根据 rule 获取规则匹配集合
        """
        official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_3, name='name', email='email@email.com', original='original', wechat='wechat')

        rule = Rule.manager.add(official_account=official_account, name='rule one', reply_pattern=Rule.REPLY_PATTERN_ALL)
        rule_match_1 = RuleMatch.manager.add(rule=rule, plugin_iden='text', order=5, status=True)
        rule_match_2 = RuleMatch.manager.add(rule=rule, plugin_iden='text', order=4, status=True)
        rule_match_3 = RuleMatch.manager.add(rule=rule, plugin_iden='text', order=1, status=True)
        rule_match_4 = RuleMatch.manager.add(rule=rule, plugin_iden='text', order=2, status=True)
        rule_match_5 = RuleMatch.manager.add(rule=rule, plugin_iden='text', order=3, status=False)
        rule_match_queryset = RuleMatch.manager.get(rule=rule)
        self.assertEqual(4, rule_match_queryset.count())
        self.assertEqual(rule_match_queryset[0], rule_match_1)
        self.assertEqual(rule_match_queryset[1], rule_match_2)
        self.assertEqual(rule_match_queryset[2], rule_match_4)
        self.assertEqual(rule_match_queryset[3], rule_match_3)
