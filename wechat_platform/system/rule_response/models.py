# -*- coding: utf-8 -*-

from django.db import models

from system.rule.models import Rule


class RuleResponseManager(models.Manager):
    """
    微信规则回复表 Manager
    """
    def add(self, rule, plugin_iden, reply_id=0, order=0, status=True):
        """
        添加微信规则回复
        """
        return super(RuleResponseManager, self).create(
            rule=rule,
            plugin_iden=plugin_iden,
            reply_id=reply_id,
            order=order,
            status=status
        )


class RuleResponse(models.Model):
    """
    微信规则回复表
    """
    rule = models.ForeignKey(Rule, verbose_name=u'所属规则')
    plugin_iden = models.CharField(u'响应插件标识符', max_length=50)
    reply_id = models.PositiveIntegerField(u'响应ID号', default=0)
    order = models.PositiveIntegerField(u'优先级', default=0)
    status = models.BooleanField(u'是否启用', default=True)

    objects = models.Manager()
    manager = RuleResponseManager()

    class Meta:
        verbose_name = u'微信规则回复表'
        verbose_name_plural = u'微信规则回复表'
        db_table = 'wechat_rule_response'

    def __unicode__(self):
        return self.plugin_iden
