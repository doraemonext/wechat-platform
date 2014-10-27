# -*- coding: utf-8 -*-

from django.db import models


class PluginManager(models.Manager):
    def add(self, iden, name, status=False, description=None, author=None, website=None, email=None, version=None):
        """
        添加一个新的插件
        :param iden: 插件标识符
        :param name: 插件名称
        :param status: 是否启用, 默认不启用
        :param description: 插件描述
        :param author: 插件作者
        :param website: 插件作者网站
        :param email: 插件作者邮箱
        :param version: 插件版本
        :return:
        """
        return super(PluginManager, self).create(
            iden=iden,
            name=name,
            status=status,
            description=description,
            author=author,
            website=website,
            email=email,
            version=version
        )


class Plugin(models.Model):
    iden = models.CharField(u'插件标识符', max_length=50, primary_key=True)
    name = models.CharField(u'插件名称', max_length=100)
    status = models.BooleanField(u'是否启用', default=False)
    description = models.TextField(u'插件描述', blank=True, null=True)
    author = models.CharField(u'插件作者', max_length=50, blank=True, null=True)
    website = models.URLField(u'插件作者网站', blank=True, null=True)
    email = models.EmailField(u'插件作者邮箱', blank=True, null=True)
    version = models.CharField(u'插件版本', max_length=30, blank=True, null=True)

    objects = models.Manager()
    manager = PluginManager()

    class Meta:
        verbose_name = u'插件表'
        verbose_name_plural = u'插件表'
        db_table = 'wechat_plugin'

    def __unicode__(self):
        return self.name