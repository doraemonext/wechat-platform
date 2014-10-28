# -*- coding: utf-8 -*-

from system.core.test import WechatTestCase
from system.library.text.models import LibraryText


class LibraryTextTest(WechatTestCase):
    def test_add_text(self):
        """
        测试添加新的文字素材
        """
        self.assertEqual(0, LibraryText.objects.count())
        text = LibraryText.manager.add(content=u'你好吗')
        self.assertEqual(1, LibraryText.objects.count())
        self.assertEqual(text.content, u'你好吗')