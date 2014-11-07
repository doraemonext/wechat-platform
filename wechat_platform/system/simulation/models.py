# -*- coding: utf-8 -*-

from django.db import models

from system.official_account.models import OfficialAccount


class SimulationMatchManager(models.Manager):
    """
    模拟登陆关系对应表
    """
    def get(self, official_account, openid=None, fakeid=None):
        """
        获取模拟登陆关系

        openid 和 fakeid 至少传入一个
        :param official_account: 公众号实例 (OfficialAccount)
        :param openid: 用户 OpenID
        :param fakeid: 用户 FakeID
        """
        if openid and fakeid:
            result = super(SimulationMatchManager, self).get_queryset().filter(
                official_account=official_account,
                openid=openid,
                fakeid=fakeid,
            )
        elif openid:
            result = super(SimulationMatchManager, self).get_queryset().filter(
                official_account=official_account,
                openid=openid,
            )
        elif fakeid:
            result = super(SimulationMatchManager, self).get_queryset().filter(
                official_account=official_account,
                fakeid=fakeid,
            )
        else:
            raise AttributeError('Requires at least one parameter in openid and fakeid')

        if result:
            return result[0]
        else:
            return None

    def add(self, official_account, openid, fakeid):
        """
        添加新的模拟登陆关系
        :param official_account: 公众号实例 (OfficialAccount)
        :param openid: 用户 OpenID
        :param fakeid: 用户 FakeID
        """
        match = super(SimulationMatchManager, self).get_queryset().filter(
            official_account=official_account,
        ).filter(
            openid=openid
        ).filter(
            fakeid=fakeid
        )

        if not match:
            return super(SimulationMatchManager, self).create(
                official_account=official_account,
                openid=openid,
                fakeid=fakeid,
            )
        else:
            return match[0]


class SimulationMatch(models.Model):
    """
    模拟登陆关系对应表
    """
    official_account = models.ForeignKey(OfficialAccount, verbose_name=u'所属公众号')
    openid = models.CharField(u'用户OpenID', max_length=50)
    fakeid = models.CharField(u'用户FakeID', max_length=50)

    objects = models.Manager()
    manager = SimulationMatchManager()

    class Meta:
        verbose_name = u'模拟登陆关系对应表'
        verbose_name_plural = u'模拟登陆关系对应表'
        db_table = 'simulation_match'

    def __unicode__(self):
        return self.openid + '-' + self.fakeid