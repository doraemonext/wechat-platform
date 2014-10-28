# -*- coding: utf-8 -*-

from django.db import models


class LibraryTextManager(models.Manager):
    """
    素材库 - 文字表 Manager
    """
    def add(self, content):
        """
        添加一条新的文字记录
        """
        return super(LibraryTextManager, self).create(content=content)


class LibraryText(models.Model):
    """
    素材库 - 文字表
    """
    content = models.TextField(u'文字')

    objects = models.Manager()
    manager = LibraryTextManager()

    class Meta:
        verbose_name = u'素材库 - 文字表'
        verbose_name_plural = u'素材库 - 文字表'
        db_table = 'library_text'

    def __unicode__(self):
        return self.content