# -*- coding: utf-8 -*-

from system.core.test import WechatTestCase
from system.official_account.models import OfficialAccount
from system.library.music.models import LibraryMusic


class LibraryMusicTest(WechatTestCase):
    def test_add_music(self):
        """
        测试添加新的音乐素材
        """
        official_account = self.make_official_account(level=OfficialAccount.LEVEL_2)
        music = LibraryMusic.manager.add(
            official_account=official_account,
            plugin_iden='music',
            title='music',
            description='description',
            music_url='http://www.google.com',
            hq_music_url='http://www.music.com',
        )
        self.assertEqual(music.official_account, official_account)
        self.assertEqual(music.plugin_iden, 'music')
        self.assertEqual(music.title, 'music')
        self.assertEqual(music.description, 'description')
        self.assertEqual(music.music_url, 'http://www.google.com')
        self.assertEqual(music.hq_music_url, 'http://www.music.com')