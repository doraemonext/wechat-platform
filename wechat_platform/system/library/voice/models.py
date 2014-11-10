# -*- coding: utf-8 -*-

from django.db import models
from django.core.files import File

from system.official_account.models import OfficialAccount
from system.simulation import Simulation, SimulationException


class LibraryVoiceManager(models.Manager):
    """
    素材库 - 语音库 Manager
    """
    def get(self, official_account, plugin_iden, voice_id):
        """
        获取一条语音
        :param official_account: 所属公众号 (OfficialAccount)
        :param plugin_iden: 所属插件标识符
        :param voice_id: 语音在库中的ID
        :return: 语音实例 (LibraryVoice)
        """
        return super(LibraryVoiceManager, self).get_queryset().filter(
            official_account=official_account
        ).filter(
            plugin_iden=plugin_iden
        ).get(
            pk=voice_id
        )

    def add(self, official_account, plugin_iden, file_path):
        """
        添加一条语音
        :param official_account: 所属公众号 (OfficialAccount)
        :param plugin_iden: 所属插件标识符
        :param file_path: 语音文件路径
        """
        f = open(file_path, 'rb')
        voice_file = File(f)
        voice = super(LibraryVoiceManager, self).create(
            official_account=official_account,
            plugin_iden=plugin_iden,
            voice=voice_file,
        )
        voice_file.close()
        f.close()
        return voice


class LibraryVoice(models.Model):
    """
    素材库 - 语音库
    """
    official_account = models.ForeignKey(OfficialAccount, verbose_name=u'所属公众号')
    plugin_iden = models.CharField(u'所属插件标识符', max_length=50)
    voice = models.FileField(u'语音本地存储位置', upload_to='library/voice')
    fid = models.BigIntegerField(u'远程素材库中的文件ID', default=0)
    media_id = models.CharField(u'语音的媒体ID', max_length=50, null=True, blank=True)

    objects = models.Manager()
    manager = LibraryVoiceManager()

    class Meta:
        verbose_name = u'素材库 - 语音库'
        verbose_name_plural = u'素材库 - 语音库'
        db_table = 'library_voice'

    def __unicode__(self):
        return self.voice

    def update_fid(self, simulation):
        """
        更新语音文件ID
        :param simulation: 模拟登陆实例
        :return: 语音文件ID
        """
        if not self.voice:  # 当本地没有存储语音时, 清空 fid
            self.fid = 0
            self.save()
            return self.fid

        try:
            fid = simulation.upload_file(filepath=self.voice.path)
            self.fid = int(fid)
        except SimulationException:  # 出现模拟登录错误时放弃上传
            self.fid = 0
        self.save()
        return self.fid