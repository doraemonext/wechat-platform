# -*- coding: utf-8 -*-

from django.db import models
from django.core.files import File

from system.official_account.models import OfficialAccount
from system.simulation import Simulation, SimulationException


class LibraryPictureManager(models.Manager):
    """
    素材库 - 图片库 Manager
    """
    def get(self, official_account, plugin_iden, picture_id):
        """
        获取一张图片
        :param official_account: 所属公众号 (OfficialAccount)
        :param plugin_iden: 所属插件标识符
        :param picture_id: 图片在库中的ID
        :return: 图片实例 (LibraryPicture)
        """
        return super(LibraryPictureManager, self).get_queryset().filter(
            official_account=official_account
        ).filter(
            plugin_iden=plugin_iden
        ).get(
            pk=picture_id
        )

    def add(self, official_account, plugin_iden, file_path):
        """
        添加一张图片
        :param official_account: 所属公众号 (OfficialAccount)
        :param plugin_iden: 所属插件标识符
        :param file_path: 图片文件路径
        """
        f = open(file_path, 'rb')
        picture_file = File(f)
        voice = super(LibraryPictureManager, self).create(
            official_account=official_account,
            plugin_iden=plugin_iden,
            picture=picture_file,
        )
        picture_file.close()
        f.close()
        return voice


class LibraryPicture(models.Model):
    """
    素材库 - 图片库
    """
    official_account = models.ForeignKey(OfficialAccount, verbose_name=u'所属公众号')
    plugin_iden = models.CharField(u'所属插件标识符', max_length=50)
    picture = models.ImageField(u'图片本地存储位置', upload_to='library/picture')
    fid = models.BigIntegerField(u'远程素材库中的文件ID', default=0)
    media_id = models.CharField(u'图片的媒体ID', max_length=50, null=True, blank=True)

    objects = models.Manager()
    manager = LibraryPictureManager()

    class Meta:
        verbose_name = u'素材库 - 图片库'
        verbose_name_plural = u'素材库 - 图片库'
        db_table = 'library_picture'

    def __unicode__(self):
        return self.picture

    def update_fid(self, simulation):
        """
        更新图片文件ID
        :param simulation: 模拟登陆实例
        :return: 图片文件ID
        """
        if not self.picture:  # 当本地没有存储图片时, 清空 fid
            self.fid = 0
            self.save()
            return self.fid

        try:
            fid = simulation.upload_file(filepath=self.picture.path)
            self.fid = int(fid)
        except SimulationException:  # 出现模拟登录错误时放弃上传
            self.fid = 0
        self.save()
        return self.fid