# -*- coding: utf-8 -*-

from wechat_sdk import WechatBasic
from wechat_sdk.context.framework.django import DatabaseContextStore

from system.core.exceptions import PluginLoadError
from system.core.test import WechatTestCase
from system.plugin.models import Plugin
from system.official_account.models import OfficialAccount
from .framework import load_plugin


class PluginTest(WechatTestCase):
    def test_add_plugin(self):
        """
        测试添加新插件
        """
        iden = u'test_plugin_iden'
        name = u'伟大的插件'
        status = True
        description = u'这里是插件的描述'
        author = u'插件作者'
        website = u'http://oott.me',
        email = u'doraemonext@gmail.com'
        version = u'1.0.0'

        self.assertEqual(0, Plugin.objects.count())
        plugin = Plugin.manager.add(
            iden=iden,
            name=name,
            status=status,
            description=description,
            author=author,
            website=website,
            email=email,
            version=version
        )
        self.assertEqual(1, Plugin.objects.count())
        self.assertEqual(iden, plugin.iden)
        self.assertEqual(name, plugin.name)
        self.assertEqual(status, plugin.status)
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