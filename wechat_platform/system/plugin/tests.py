# -*- coding: utf-8 -*-

from wechat_sdk import WechatBasic
from wechat_sdk.context.framework.django import DatabaseContextStore

from system.core.exceptions import PluginLoadError, PluginDoesNotExist
from system.core.test import WechatTestCase
from system.plugin.models import Plugin
from system.official_account.models import OfficialAccount
from .framework import load_plugin


class PluginTest(WechatTestCase):
    def test_get_plugin(self):
        """
        测试获取插件
        """
        official_account_1 = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_1, name='Ace Kwok', email='doraemonext@gmail.com', original='original', wechat='wechat')
        official_account_2 = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_2, name='doraemonext', email='doraemonext@gmail.com', original='original', wechat='wechat')
        plugin_1 = Plugin.manager.add(iden='myplugin1', name=u'测试插件1')
        plugin_1.official_account.add(official_account_1)
        plugin_2 = Plugin.manager.add(iden='myplugin2', name=u'测试插件2')
        plugin_2.official_account.add(official_account_2)
        plugin_3 = Plugin.manager.add(iden='myplugin3', name=u'测试插件3')
        plugin_3.official_account.add(official_account_1, official_account_2)
        plugin_4 = Plugin.manager.add(iden='myplugin4', name=u'测试插件4')

        self.assertEqual(Plugin.manager.get(official_account=official_account_1, iden='myplugin1'), plugin_1)
        self.assertEqual(Plugin.manager.get(official_account=official_account_2, iden='myplugin2'), plugin_2)
        self.assertEqual(Plugin.manager.get(official_account=official_account_1, iden='myplugin3'), plugin_3)
        self.assertEqual(Plugin.manager.get(official_account=official_account_2, iden='myplugin3'), plugin_3)
        with self.assertRaises(PluginDoesNotExist):
            Plugin.manager.get(official_account=official_account_1, iden='myplugin2')
        with self.assertRaises(PluginDoesNotExist):
            Plugin.manager.get(official_account=official_account_2, iden='myplugin1')
        with self.assertRaises(PluginDoesNotExist):
            Plugin.manager.get(official_account=official_account_1, iden='myplugin4')
        with self.assertRaises(PluginDoesNotExist):
            Plugin.manager.get(official_account=official_account_2, iden='myplugin4')

    def test_add_plugin(self):
        """
        测试添加新插件
        """
        iden = u'test_plugin_iden'
        name = u'伟大的插件'
        description = u'这里是插件的描述'
        author = u'插件作者'
        website = u'http://oott.me',
        email = u'doraemonext@gmail.com'
        version = u'1.0.0'

        self.assertEqual(0, Plugin.objects.count())
        plugin = Plugin.manager.add(
            iden=iden,
            name=name,
            description=description,
            author=author,
            website=website,
            email=email,
            version=version
        )
        self.assertEqual(1, Plugin.objects.count())
        self.assertEqual(iden, plugin.iden)
        self.assertEqual(name, plugin.name)
        self.assertEqual(description, plugin.description)
        self.assertEqual(author, plugin.author)
        self.assertEqual(website, plugin.website)
        self.assertEqual(email, plugin.email)
        self.assertEqual(version, plugin.version)

    def test_load_system_plugin_with_error_plugin_iden(self):
        official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_2, name='Ace Kwok', email='doraemonext@gmail.com', original='original', wechat='wechat')
        wechat = WechatBasic(token='random_token')
        wechat.parse_data(data=self.make_raw_text_message())
        context = DatabaseContextStore(openid=self.make_source())
        message = wechat.get_message()

        plugin = Plugin.manager.add(iden='text_failed', name=u'系统文字回复插件')
        with self.assertRaises(PluginLoadError):
            plugin_loaded = load_plugin(
                official_account=official_account,
                wechat=wechat,
                context=context,
                message=message,
                in_context=False,
                is_exclusive=False,
                plugin=plugin,
                is_system=True
            )

    def test_load_system_plugin_with_error_type(self):
        official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_2, name='Ace Kwok', email='doraemonext@gmail.com', original='original', wechat='wechat')
        wechat = WechatBasic(token='random_token')
        wechat.parse_data(data=self.make_raw_text_message())
        context = DatabaseContextStore(openid=self.make_source())
        message = wechat.get_message()

        plugin = Plugin.manager.add(iden='text', name=u'系统文字回复插件')
        with self.assertRaises(PluginLoadError):
            plugin_loaded = load_plugin(
                official_account=official_account,
                wechat=wechat,
                context=context,
                message=message,
                in_context=False,
                is_exclusive=False,
                plugin=plugin,
                is_system=False
            )

    def test_load_system_plugin(self):
        official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_2, name='Ace Kwok', email='doraemonext@gmail.com', original='original', wechat='wechat')
        wechat = WechatBasic(token='random_token')
        wechat.parse_data(data=self.make_raw_text_message())
        context = DatabaseContextStore(openid=self.make_source())
        message = wechat.get_message()

        plugin = Plugin.manager.add(iden='text', name=u'系统文字回复插件')
        plugin_loaded = load_plugin(
            official_account=official_account,
            wechat=wechat,
            context=context,
            message=message,
            in_context=False,
            is_exclusive=False,
            plugin=plugin,
            is_system=True
        )

        self.assertEqual(plugin_loaded.official_account, official_account)
        self.assertEqual(plugin_loaded.wechat, wechat)
        self.assertEqual(plugin_loaded.context, context)
        self.assertEqual(plugin_loaded.message, message)
        self.assertFalse(plugin_loaded.in_context)
        self.assertFalse(plugin_loaded.is_exclusive)
        self.assertEqual(plugin_loaded.plugin, plugin)
        self.assertTrue(plugin_loaded.is_system)