# -*- coding: utf-8 -*-

from django.db import models


class SettingManager(models.Manager):
    def add(self, name, value):
        """
        添加一条新的设置项
        :param name: 名称
        :param value: 内容
        :return: Setting实例
        """
        return super(SettingManager, self).create(name=name, value=value)

    def get(self, name):
        """
        根据name获取对应的选项内容
        :param name: 选项名称
        :return: 选项内容
        """
        return super(SettingManager, self).get_queryset().get(name=name).value

    def get_all(self):
        """
        获取所有的设置并以字典的形式返回
        :return: dict对象
        """
        settings = super(SettingManager, self).get_queryset().all()
        result = {}
        for item in settings:
            result[item.name] = item.value
        return result


class Setting(models.Model):
    name = models.CharField(u'选项名称', max_length=64, unique=True)
    value = models.TextField(u'选项内容')

    objects = models.Manager()
    manager = SettingManager()

    class Meta:
        verbose_name = u'系统设置'
        verbose_name_plural = u'系统设置'
        db_table = 'setting'
