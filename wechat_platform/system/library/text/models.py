# -*- coding: utf-8 -*-

from django.db import models

from system.official_account.models import OfficialAccount


class LibraryTextManager(models.Manager):
    """
    素材库 - 文字库 Manager
    """
    def get(self, official_account, plugin_iden, text_id):
        """
        获取一条文字素材
        :param official_account: 所属公众号 (OfficialAccount)
        :param plugin_iden: 所属插件标识符
        :param text_id: 对应文字在本地素材库中的ID
        :return: 文字实例 (LibraryText)
        """
        return super(LibraryTextManager, self).get_queryset().filter(
            official_account=official_account
        ).filter(
            plugin_iden=plugin_iden
        ).get(
            pk=text_id
        )

    def add(self, official_account, plugin_iden, content):
        """
        添加一条新的文字素材
        :param official_account: 所属公众号
        :param plugin_iden: 所属插件标识符
        :param content: 文字内容
        """
        return super(LibraryTextManager, self).create(
            official_account=official_account,
            plugin_iden=plugin_iden,
            content=content,
        )


class LibraryText(models.Model):
    """
    素材库 - 文字库
    """
    official_account = models.ForeignKey(OfficialAccount, verbose_name=u'所属公众号')
    plugin_iden = models.CharField(u'所属插件标识符', max_length=50)
    content = models.TextField(u'文字')

    objects = models.Manager()
    manager = LibraryTextManager()

    class Meta:
        verbose_name = u'素材库 - 文字表'
        verbose_name_plural = u'素材库 - 文字表'
        db_table = 'library_text'

    def __unicode__(self):
        return self.content