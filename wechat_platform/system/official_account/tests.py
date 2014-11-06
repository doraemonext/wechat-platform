# -*- coding: utf-8 -*-

from django.test import TestCase

from system.official_account.models import OfficialAccount
from system.rule.models import Rule
from system.rule_match.models import RuleMatch
from system.library.text.models import LibraryText


class OfficialAccountTest(TestCase):
    def test_add_normal_subscription(self):
        """
        测试添加普通订阅号
        """
        account = OfficialAccount.manager.add(
            level=OfficialAccount.LEVEL_1,
            name=u'测试普通订阅号名称',
            email='doraemonext@gmail.com',
            original='gh_1b2959761b7e',
            wechat='doraemonext_pub',
            introduction=u'订阅号简介',
            address=u'订阅号地址详情',
            username='test',
            password='test',
            is_advanced=True
        )
        self.assertEqual(account.level, OfficialAccount.LEVEL_1)
        self.assertEqual(account.name, u'测试普通订阅号名称')
        self.assertEqual(account.email, 'doraemonext@gmail.com')
        self.assertEqual(account.original, 'gh_1b2959761b7e')
        self.assertEqual(account.wechat, 'doraemonext_pub')
        self.assertEqual(account.introduction, u'订阅号简介')
        self.assertEqual(account.address, u'订阅号地址详情')
        self.assertEqual(account.username, 'test')
        self.assertEqual(account.password, 'test')
        self.assertEqual(len(account.token), 32)
        self.assertIsInstance(account.token, str)
        self.assertEqual(len(account.iden), 32)
        self.assertIsInstance(account.iden, str)
        self.assertEqual(account.is_advanced, True)

        rule = Rule.objects.get(name='_system_default_' + account.iden)
        self.assertEqual(rule.official_account, account)
        self.assertEqual(rule.reply_pattern, Rule.REPLY_PATTERN_RANDOM)

        rule_match = RuleMatch.objects.filter(rule=rule)
        self.assertEqual(rule_match.count(), 1)
        self.assertEqual(rule_match[0].plugin_iden, 'text')

        library_text = LibraryText.objects.get(pk=rule_match[0].reply_id)
        self.assertEqual(library_text.official_account, account)
        self.assertEqual(library_text.content, u'此处为默认回复内容，请在后台更改')

    def test_add_normal_service(self):
        """
        测试添加认证订阅号/普通服务号
        """
        account = OfficialAccount.manager.add(
            level=OfficialAccount.LEVEL_2,
            name=u'测试认证订阅号/普通服务号名称',
            email='doraemonext@gmail.com',
            original='gh_1b2959761b7e',
            wechat='doraemonext_pub',
            introduction=u'订阅号简介',
            address=u'订阅号地址详情',
            username='test',
            password='test',
            is_advanced=False,
            appid='wxf32sf34ed2ccc2ab',
            appsecret='087sa087a9c087e07'
        )
        self.assertEqual(account.level, OfficialAccount.LEVEL_2)
        self.assertEqual(account.name, u'测试认证订阅号/普通服务号名称')
        self.assertEqual(account.email, 'doraemonext@gmail.com')
        self.assertEqual(account.original, 'gh_1b2959761b7e')
        self.assertEqual(account.wechat, 'doraemonext_pub')
        self.assertEqual(account.introduction, u'订阅号简介')
        self.assertEqual(account.address, u'订阅号地址详情')
        self.assertEqual(account.username, 'test')
        self.assertEqual(account.password, 'test')
        self.assertEqual(account.is_advanced, False)
        self.assertEqual(account.appid, 'wxf32sf34ed2ccc2ab')
        self.assertEqual(account.appsecret, '087sa087a9c087e07')
        self.assertEqual(len(account.token), 32)
        self.assertIsInstance(account.token, str)
        self.assertEqual(len(account.iden), 32)
        self.assertIsInstance(account.iden, str)

    def test_add_auth_service(self):
        """
        测试添加认证服务号
        """
        account = OfficialAccount.manager.add(
            level=OfficialAccount.LEVEL_3,
            name=u'测试认证订阅号/普通服务号名称',
            email='doraemonext@gmail.com',
            original='gh_1b2959761b7e',
            wechat='doraemonext_pub',
            introduction=u'订阅号简介',
            address=u'订阅号地址详情',
            username='test',
            password='test',
            is_advanced=True,
            appid='wxf32sf34ed2ccc2ab',
            appsecret='087sa087a9c087e07'
        )
        self.assertEqual(account.level, OfficialAccount.LEVEL_3)
        self.assertEqual(account.name, u'测试认证订阅号/普通服务号名称')
        self.assertEqual(account.email, 'doraemonext@gmail.com')
        self.assertEqual(account.original, 'gh_1b2959761b7e')
        self.assertEqual(account.wechat, 'doraemonext_pub')
        self.assertEqual(account.introduction, u'订阅号简介')
        self.assertEqual(account.address, u'订阅号地址详情')
        self.assertEqual(account.username, 'test')
        self.assertEqual(account.password, 'test')
        self.assertEqual(account.is_advanced, True)
        self.assertEqual(account.appid, 'wxf32sf34ed2ccc2ab')
        self.assertEqual(account.appsecret, '087sa087a9c087e07')
        self.assertEqual(len(account.token), 32)
        self.assertIsInstance(account.token, str)
        self.assertEqual(len(account.iden), 32)
        self.assertIsInstance(account.iden, str)