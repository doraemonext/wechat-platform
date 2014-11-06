# -*- coding: utf-8 -*-

import logging

from django.db import models

from system.official_account.models import OfficialAccount

logger_rule = logging.getLogger(__name__)


class RuleManager(models.Manager):
    def add(self, official_account, name, reply_pattern, status=True, top=False, order=0):
        """
        添加一条新的规则
        :param official_account: 所属公众号
        :param name: 规则名称
        :param reply_pattern: 回复方式
        :param status: 是否启用, 默认启用
        :param top: 是否置顶, 默认不置顶
        :param order: 优先级，默认为0
        :return: 规则 Rule 实例
        """
        rule = super(RuleManager, self).create(
            official_account=official_account,
            name=name,
            reply_pattern=reply_pattern,
            status=status,
            top=top,
            order=order
        )
        logger_rule.info('New rule created [Detail] %s' % rule.__dict__)
        return rule


class Rule(models.Model):
    """
    微信规则表
    """
    REPLY_PATTERN_ALL = 0
    REPLY_PATTERN_RANDOM = 1
    REPLY_PATTERN_FORWARD = 2
    REPLY_PATTERN_REVERSE = 3
    REPLY_PATTERN = (
        (REPLY_PATTERN_ALL, u'全部回复'),
        (REPLY_PATTERN_RANDOM, u'随机回复'),
        (REPLY_PATTERN_FORWARD, u'顺序回复'),
        (REPLY_PATTERN_REVERSE, u'逆序回复'),
    )

    official_account = models.ForeignKey(OfficialAccount, verbose_name=u'所属公众号')
    name = models.CharField(u'规则名称', max_length=50)
    reply_pattern = models.IntegerField(u'回复方式', choices=REPLY_PATTERN, default=REPLY_PATTERN_RANDOM)
    status = models.BooleanField(u'是否启用', default=True)
    top = models.BooleanField(u'是否置顶', default=False)
    order = models.PositiveIntegerField(u'优先级', default=0)

    objects = models.Manager()
    manager = RuleManager()

    class Meta:
        verbose_name = u'微信规则表'
        verbose_name_plural = u'微信规则表'
        db_table = 'wechat_rule'

    def __unicode__(self):
        return self.name