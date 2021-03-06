# -*- coding: utf-8 -*-

import logging
from operator import attrgetter

from django.db import models

from system.official_account.models import OfficialAccount
from system.rule.models import Rule

logger_keyword = logging.getLogger(__name__)


class KeywordManager(models.Manager):
    """
    微信关键字表 Manager
    """
    def add(self, rule, keyword, status=True, type=0):
        """
        添加新的关键字
        :param rule: 所属规则
        :param keyword: 关键字
        :param status: 是否启用
        :param type: 关键字类型
        :return: Keyword 实例
        """
        keyword = super(KeywordManager, self).create(
            official_account=rule.official_account,
            rule=rule,
            keyword=keyword,
            status=status,
            type=type
        )
        logger_keyword.info('New keyword created [Detail] %s' % keyword.__dict__)
        return keyword

    def search(self, official_account, keyword):
        """
        根据用户请求中的文本内容在关键字表中进行数据库检索, 并返回对应的关键字实例
        :param official_account: 所属公众号
        :param keyword: 请求查询的文本内容
        :return: Keyword 实例
        """
        # 进行完全匹配搜索
        result_full = super(KeywordManager, self).get_queryset().filter(
            official_account=official_account
        ).filter(
            status=True
        ).filter(
            type=self.model.TYPE_FULL
        ).filter(
            keyword=keyword
        ).filter(
            rule__status=True
        ).order_by(
            '-rule__top'
        ).order_by(
            '-rule__order'
        )[:1]

        # 进行包含匹配搜索
        result_contain = super(KeywordManager, self).raw(" \
        SELECT keyword.id AS id, keyword.rule_id AS rule_id, \
        keyword.keyword AS keyword FROM {keyword_table} AS keyword \
        LEFT JOIN {rule_table} AS rule ON keyword.rule_id = rule.id \
        WHERE keyword.official_account_id={official_account_id} AND rule.status='1' \
        AND keyword.status='1' AND keyword.type='{keyword_type}' \
        AND INSTR(%s, `keyword`) > 0 ORDER BY rule.top DESC, rule.order DESC \
        LIMIT 1".format(
            keyword_table=Keyword._meta.db_table,
            rule_table=Rule._meta.db_table,
            official_account_id=official_account.pk,
            keyword_type=self.model.TYPE_CONTAIN
        ), [keyword])

        # 进行正则匹配搜索
        result_regex = super(KeywordManager, self).raw(" \
        SELECT keyword.id AS id, keyword.rule_id AS rule_id, \
        keyword.keyword AS keyword FROM {keyword_table} AS keyword \
        LEFT JOIN {rule_table} AS rule ON keyword.rule_id = rule.id \
        WHERE keyword.official_account_id={official_account_id} \
        AND rule.status='1' AND keyword.status='1' AND keyword.type='{keyword_type}' \
        AND %s REGEXP `keyword` ORDER BY rule.top DESC, rule.order DESC \
        LIMIT 1".format(
            keyword_table=Keyword._meta.db_table,
            rule_table=Rule._meta.db_table,
            official_account_id=official_account.pk,
            keyword_type=self.model.TYPE_REGEX
        ), [keyword])

        # 取得查询所得结果并排序, 按照rule选择优先级最高的一个作为结果返回
        result = list()
        if result_full:
            result.append(result_full[0])
        for item in result_contain:
            result.append(Keyword.objects.get(pk=item.id))
        for item in result_regex:
            result.append(Keyword.objects.get(pk=item.id))
        sorted(result, key=attrgetter('rule.top', 'rule.order'), reverse=True)

        if result:
            return result[0]
        else:
            return None


class Keyword(models.Model):
    """
    微信关键字表
    """
    TYPE_FULL = 0
    TYPE_CONTAIN = 1
    TYPE_REGEX = 2
    TYPE = (
        (TYPE_FULL, u'完全匹配'),
        (TYPE_CONTAIN, u'包含匹配'),
        (TYPE_REGEX, u'正则表达式匹配'),
    )

    official_account = models.ForeignKey(OfficialAccount, verbose_name=u'所属公众号')
    rule = models.ForeignKey(Rule, verbose_name=u'所属规则')
    keyword = models.CharField(u'关键字', max_length=255)
    status = models.BooleanField(u'是否启用', default=True)
    type = models.IntegerField(u'关键字类型', choices=TYPE, default=TYPE_FULL)

    objects = models.Manager()
    manager = KeywordManager()

    class Meta:
        verbose_name = u'微信关键字表'
        verbose_name_plural = u'微信关键字表'
        db_table = 'wechat_keyword'

    def __unicode__(self):
        return self.keyword