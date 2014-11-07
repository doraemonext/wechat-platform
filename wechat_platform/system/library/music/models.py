# -*- coding: utf-8 -*-

from django.db import models

from system.official_account.models import OfficialAccount


class LibraryMusicManager(models.Manager):
    """
    素材库 - 音乐库 Manager
    """
    def add(self, official_account, title=None, description=None, music_url=None, hq_music_url=None,
            thumb_media_id=None, music=None, hq_music=None, thumb_media=None):
        """
        添加一条新的音乐素材
        """
        return super(LibraryMusicManager, self).create(
            official_account=official_account,
            title=title,
            description=description,
            music_url=music_url,
            hq_music_url=hq_music_url,
            thumb_media_id=thumb_media_id,
            music=music,
            hq_music=hq_music,
            thumb_media=thumb_media,
        )


class LibraryMusic(models.Model):
    """
    素材库 - 音乐库
    """
    official_account = models.ForeignKey(OfficialAccount, verbose_name=u'所属公众号')
    title = models.CharField(u'音乐标题', max_length=255, blank=True, null=True)
    description = models.TextField(u'音乐描述', blank=True, null=True)
    music_url = models.CharField(u'音乐URL', max_length=1024, blank=True, null=True)
    hq_music_url = models.CharField(u'高清音乐URL', max_length=1024, blank=True, null=True)
    thumb_media_id = models.CharField(u'缩略图媒体ID', max_length=255, blank=True, null=True)
    music = models.FileField(u'音乐文件', upload_to='library/music', blank=True, null=True)
    hq_music = models.FileField(u'高清音乐文件', upload_to='library/music/hq', blank=True, null=True)
    thumb_media = models.ImageField(u'缩略图媒体图像', upload_to='library/music/thumb', blank=True, null=True)

    objects = models.Manager()
    manager = LibraryMusicManager()

    class Meta:
        verbose_name = u'素材库 - 音乐库'
        verbose_name_plural = u'素材库 - 音乐库'
        db_table = 'library_music'

    def __unicode__(self):
        return self.content
