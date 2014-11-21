# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse

from system.official_account.models import OfficialAccount
from system.media.models import Media


class LibraryMusicManager(models.Manager):
    """
    素材库 - 音乐库 Manager
    """
    def get(self, official_account, plugin_iden, music_id):
        """
        获取一首音乐
        :param official_account: 所属公众号 (OfficialAccount)
        :param plugin_iden: 所属插件标识符
        :param music_id: 音乐在库中的ID
        :return: 音乐实例 (LibraryMusic)
        """
        return super(LibraryMusicManager, self).get_queryset().filter(
            official_account=official_account
        ).filter(
            plugin_iden=plugin_iden
        ).get(
            pk=music_id
        )

    def add(self, official_account, plugin_iden, title=None, description=None, music_url=None, hq_music_url=None,
            thumb_media_id=None, music=None, hq_music=None, thumb=None):
        """
        添加一条新的音乐素材
        """
        if not music_url and music:
            music_url = reverse('filetranslator:download', kwargs={'key': music.pk})
        if not hq_music_url and hq_music:
            hq_music_url = reverse('filetranslator:download', kwargs={'key': hq_music.pk})
        if not thumb_media_id and thumb:
            pass  # TODO: 待开发

        return super(LibraryMusicManager, self).create(
            official_account=official_account,
            plugin_iden=plugin_iden,
            title=title,
            description=description,
            music_url=music_url,
            hq_music_url=hq_music_url,
            thumb_media_id=thumb_media_id,
            music=music,
            hq_music=hq_music,
            thumb=thumb,
        )


class LibraryMusic(models.Model):
    """
    素材库 - 音乐库
    """
    official_account = models.ForeignKey(OfficialAccount, verbose_name=u'所属公众号')
    plugin_iden = models.CharField(u'所属插件标识符', max_length=50)
    title = models.CharField(u'音乐标题', max_length=255, blank=True, null=True)
    description = models.TextField(u'音乐描述', blank=True, null=True)
    music_url = models.CharField(u'音乐URL', max_length=1024, blank=True, null=True)
    hq_music_url = models.CharField(u'高清音乐URL', max_length=1024, blank=True, null=True)
    thumb_media_id = models.CharField(u'缩略图媒体ID', max_length=255, blank=True, null=True)
    music = models.ForeignKey(Media, related_name='+', verbose_name=u'音乐文件', blank=True, null=True, on_delete=models.SET_NULL)
    hq_music = models.ForeignKey(Media, related_name='+', verbose_name=u'高清音乐文件', blank=True, null=True, on_delete=models.SET_NULL)
    thumb = models.ForeignKey(Media, related_name='+', verbose_name=u'缩略图媒体图像', blank=True, null=True, on_delete=models.SET_NULL)

    objects = models.Manager()
    manager = LibraryMusicManager()

    class Meta:
        verbose_name = u'素材库 - 音乐库'
        verbose_name_plural = u'素材库 - 音乐库'
        db_table = 'library_music'

    def __unicode__(self):
        return self.content
