# -*- coding: utf-8 -*-

from system.core.test import WechatTestCase
from system.official_account.models import OfficialAccount
from system.library.text.models import LibraryText


class LibraryTextTest(WechatTestCase):
    def test_add_text(self):
        """
        测试添加新的文字素材
        """
        official_account = self.make_official_account(level=OfficialAccount.LEVEL_2)
        text = LibraryText.manager.add(
            official_account=official_account,
            plugin_iden='text',
            content=u'你好吗',
        )
        self.assertEqual(text.official_account, official_account)
        self.assertEqual(text.content, u'你好吗')