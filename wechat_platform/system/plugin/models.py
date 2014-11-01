# -*- coding: utf-8 -*-

from django.db import models

from system.core.exceptions import PluginDoesNotExist
from system.official_account.models import OfficialAccount


class PluginManager(models.Manager):
    def get(self, official_account, iden):
        """
        获取插件实例
        :param official_account: 所属公众号
        :param iden: 插件标识符
        :return: 如果插件存在, 返回插件实例 (Plugin)
        :raise PluginDoesNotExist: 当不存在该插件或该插件在所属公众号中没有开启则抛出此异常
        """
        plugin = super(PluginManager, self).get_queryset().filter(pk=iden)
        if not plugin:
            raise PluginDoesNotExist('the plugin iden does not exist')
        if official_account not in plugin[0].official_account.all():
            raise PluginDoesNotExist('the plugin is not enabled in the official account')
        return plugin[0]

    def add(self, iden, name, description=None, author=None, website=None, email=None, version=None):
        """
        添加一个新的插件
        :param iden: 插件标识符
        :param name: 插件名称
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
            description=description,
            author=author,
            website=website,
            email=email,
            version=version
        )


class Plugin(models.Model):
    iden = models.CharField(u'插件标识符', max_length=50, primary_key=True)
    name = models.CharField(u'插件名称', max_length=100)
    description = models.TextField(u'插件描述', blank=True, null=True)
    author = models.CharField(u'插件作者', max_length=50, blank=True, null=True)
    website = models.URLField(u'插件作者网站', blank=True, null=True)
    email = models.EmailField(u'插件作者邮箱', blank=True, null=True)
    version = models.CharField(u'插件版本', max_length=30, blank=True, null=True)
    official_account = models.ManyToManyField(OfficialAccount, verbose_name=u'开启该插件的公众号集合')

    objects = models.Manager()
    manager = PluginManager()

    class Meta:
        verbose_name = u'插件表'
        verbose_name_plural = u'插件表'
        db_table = 'wechat_plugin'

    def __unicode__(self):
        return self.name