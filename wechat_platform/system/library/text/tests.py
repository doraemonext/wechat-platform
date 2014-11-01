# -*- coding: utf-8 -*-

from system.core.test import WechatTestCase
from system.official_account.models import OfficialAccount
from system.library.text.models import LibraryText


class LibraryTextTest(WechatTestCase):
    def test_add_text(self):
        """
        测试添加新的文字素材
        """
        official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_1, name='Ace Kwok', email='doraemonext@gmail.com', original='original', wechat='wechat')
        self.assertEqual(0, LibraryText.objects.count())
        text = LibraryText.manager.add(official_account, content=u'你好吗')
        self.assertEqual(1, LibraryText.objects.count())
        self.assertEqual(text.official_account, official_account)
        self.assertEqual(text.content, u'你好吗')