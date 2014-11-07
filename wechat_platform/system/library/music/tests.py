# -*- coding: utf-8 -*-

from system.core.test import WechatTestCase
from system.official_account.models import OfficialAccount
from system.library.music.models import LibraryMusic


class LibraryMusicTest(WechatTestCase):
    def test_add_music(self):
        """
        测试添加新的音乐素材
        """
        official_account = OfficialAccount.manager.add(level=OfficialAccount.LEVEL_1, name='Ace Kwok', email='doraemonext@gmail.com', original='original', wechat='wechat')
        music = LibraryMusic.manager.add(
            official_account=official_account,
            title='music',
            description='description',
            music_url='http://www.google.com',
            hq_music_url='http://www.music.com',
        )
        self.assertEqual(music.official_account, official_account)
        self.assertEqual(music.title, 'music')
        self.assertEqual(music.description, 'description')
        self.assertEqual(music.music_url, 'http://www.google.com')
        self.assertEqual(music.hq_music_url, 'http://www.music.com')