# -*- coding: utf-8 -*-

from django.db import models

from system.official_account.models import OfficialAccount
from system.media.models import Media
from system.simulation import Simulation, SimulationException


class LibraryImageManager(models.Manager):
    """
    素材库 - 图片库 Manager
    """
    def get_list(self, official_account):
        """
        获取单个公众号的所有图片列表
        :param official_account: 所属公众号
        :return: 列表, 每个元素为一个 LibraryImage 实例
        """
        return super(LibraryImageManager, self).get_queryset().filter(
            official_account=official_account
        )

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

    def add(self, official_account, plugin_iden, image):
        """
        添加一张图片
        :param official_account: 所属公众号 (OfficialAccount)
        :param plugin_iden: 所属插件标识符
        :param image: 图片文件实例 (Media)
        """
        return super(LibraryImageManager, self).create(
            official_account=official_account,
            plugin_iden=plugin_iden,
            image=image,
        )


class LibraryImage(models.Model):
    """
    素材库 - 图片库
    """
    official_account = models.ForeignKey(OfficialAccount, verbose_name=u'所属公众号')
    plugin_iden = models.CharField(u'所属插件标识符', max_length=50)
    image = models.ForeignKey(Media, related_name='+', verbose_name=u'图片文件', blank=True, null=True)
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
            fid = simulation.upload_file(filepath=self.image.media.path)
            self.fid = int(fid)
        except SimulationException:  # 出现模拟登录错误时放弃上传
            self.fid = 0
        self.save()
        return self.fid