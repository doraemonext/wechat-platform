# -*- coding: utf-8 -*-

from django.db import models
from django.core.files import File

from system.official_account.models import OfficialAccount
from system.simulation import Simulation, SimulationException


class LibraryImageManager(models.Manager):
    """
    素材库 - 图片库 Manager
    """
    def get(self, official_account, plugin_iden, image_id):
        """
        获取一张图片
        :param official_account: 所属公众号 (OfficialAccount)
        :param plugin_iden: 所属插件标识符
        :param image_id: 图片在库中的ID
        :return: 图片实例 (LibraryImage)
        """
        return super(LibraryImageManager, self).get_queryset().filter(
            official_account=official_account
        ).filter(
            plugin_iden=plugin_iden
        ).get(
            pk=image_id
        )

    def add(self, official_account, plugin_iden, file_path):
        """
        添加一张图片
        :param official_account: 所属公众号 (OfficialAccount)
        :param plugin_iden: 所属插件标识符
        :param file_path: 图片文件路径
        """
        f = open(file_path, 'rb')
        image_file = File(f)
        image = super(LibraryImageManager, self).create(
            official_account=official_account,
            plugin_iden=plugin_iden,
            image=image_file,
        )
        image_file.close()
        f.close()
        return image


class LibraryImage(models.Model):
    """
    素材库 - 图片库
    """
    official_account = models.ForeignKey(OfficialAccount, verbose_name=u'所属公众号')
    plugin_iden = models.CharField(u'所属插件标识符', max_length=50)
    image = models.ImageField(u'图片本地存储位置', upload_to='library/image')
    fid = models.BigIntegerField(u'远程素材库中的文件ID', default=0)
    media_id = models.CharField(u'图片的媒体ID', max_length=50, null=True, blank=True)

    objects = models.Manager()
    manager = LibraryImageManager()

    class Meta:
        verbose_name = u'素材库 - 图片库'
        verbose_name_plural = u'素材库 - 图片库'
        db_table = 'library_image'

    def __unicode__(self):
        return self.image

    def update_fid(self, simulation):
        """
        更新图片文件ID
        :param simulation: 模拟登陆实例
        :return: 图片文件ID
        """
        if not self.image:  # 当本地没有存储图片时, 清空 fid
            self.fid = 0
            self.save()
            return self.fid

        try:
            fid = simulation.upload_file(filepath=self.image.path)
            self.fid = int(fid)
        except SimulationException:  # 出现模拟登录错误时放弃上传
            self.fid = 0
        self.save()
        return self.fid