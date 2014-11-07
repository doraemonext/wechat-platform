# -*- coding: utf-8 -*-

from django.db import models

from system.official_account.models import OfficialAccount


class LibraryTextManager(models.Manager):
    """
    素材库 - 文字库 Manager
    """
    def add(self, official_account, content):
        """
        添加一条新的文字素材
        :param official_account: 所属公众号
        :param content: 文字内容
        """
        return super(LibraryTextManager, self).create(official_account=official_account, content=content)


class LibraryText(models.Model):
    """
    素材库 - 文字库
    """
    official_account = models.ForeignKey(OfficialAccount, verbose_name=u'所属公众号')
    content = models.TextField(u'文字')

    objects = models.Manager()
    manager = LibraryTextManager()

    class Meta:
        verbose_name = u'素材库 - 文字表'
        verbose_name_plural = u'素材库 - 文字表'
        db_table = 'library_text'

    def __unicode__(self):
        return self.content