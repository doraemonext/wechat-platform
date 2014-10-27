# -*- coding: utf-8 -*-

from system.core.test import WechatTestCase
from system.plugin.models import Plugin


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