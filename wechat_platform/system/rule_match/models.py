# -*- coding: utf-8 -*-

from django.db import models

from system.official_account.models import OfficialAccount
from system.rule.models import Rule


class RuleMatchManager(models.Manager):
    """
    微信规则回复表 Manager
    """
    def add(self, rule, plugin_iden, reply_id=0, order=0, status=True):
        """
        添加微信规则回复
        """
        return super(RuleMatchManager, self).create(
            official_account=rule.official_account,
            rule=rule,
            plugin_iden=plugin_iden,
            reply_id=reply_id,
            order=order,
            status=status
        )

    def get(self, rule):
        """
        根据 rule 返回相应的 QuerySet 集合

        返回的集合已经按照优先级排序完毕, 且剔除掉了没有启用的匹配
        """
        return super(RuleMatchManager, self).get_queryset().filter(
            official_account=rule.official_account
        ).filter(
            rule=rule
        ).filter(
            status=True
        ).order_by(
            '-order'
        )


class RuleMatch(models.Model):
    """
    微信规则匹配表
    """
    official_account = models.ForeignKey(OfficialAccount, verbose_name=u'所属公众号')
    rule = models.ForeignKey(Rule, verbose_name=u'所属规则')
    plugin_iden = models.CharField(u'响应插件标识符', max_length=50)
    reply_id = models.PositiveIntegerField(u'响应ID号', default=0)
    order = models.PositiveIntegerField(u'优先级', default=0)
    status = models.BooleanField(u'是否启用', default=True)

    objects = models.Manager()
    manager = RuleMatchManager()

    class Meta:
        verbose_name = u'微信规则匹配表'
        verbose_name_plural = u'微信规则匹配表'
        db_table = 'wechat_rule_match'

    def __unicode__(self):
        return self.plugin_iden
