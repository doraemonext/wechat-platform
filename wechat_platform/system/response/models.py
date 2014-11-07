# -*- coding: utf-8 -*-

import logging
from time import time

from django.db import models
from wechat_sdk.messages import EventMessage

from system.official_account.models import OfficialAccount

logger_response = logging.getLogger(__name__)


class ResponseManager(models.Manager):
    """
    微信服务器响应消息记录表 Manager
    """
    def get(self, official_account, msgid):
        return super(ResponseManager, self).get_queryset().filter(
            official_account=official_account
        ).filter(
            msgid=msgid
        ).exclude(
            type=Response.TYPE_WAITING
        )

    def add(self, official_account, wechat_instance, type, pattern, raw):
        """
        添加一条新的响应消息记录
        :param official_account: 微信公众号实例 (OfficialAccount)
        :param wechat_instance: 微信请求实例 (WechatBasic)
        :param type: 信息类型
        :param pattern: 响应方式
        :param raw: 原始信息内容
        """
        message = wechat_instance.get_message()
        if isinstance(message, EventMessage):
            msgid = message.target + str(message.time)
        else:
            msgid = message.id

        # 先在数据库中查找等待中的消息回复
        response = super(ResponseManager, self).get_queryset().filter(
            official_account=official_account
        ).filter(
            msgid=msgid
        ).filter(
            type=Response.TYPE_WAITING
        )
        if response:
            response = response[0]
            response.time = int(time())
            response.type = type
            response.pattern = pattern
            response.raw = raw
            response.save()
            logger_response.debug('Response has been updated [Detail: %s]' % response.__dict__)
        else:
            response = super(ResponseManager, self).create(
                official_account=official_account,
                msgid=msgid,
                target=message.source,
                source=message.target,
                time=int(time()),
                type=type,
                pattern=pattern,
                raw=raw
            )
            logger_response.debug('New response created [Detail: %s]' % response.__dict__)
        return response

    def is_waiting(self, official_account, wechat_instance):
        """
        判断该回复是否正在等待中
        :param official_account: 微信公众号实例 (OfficialAccount)
        :param wechat_instance: 微信请求实例 (WechatBasic)
        :return: 如果正在等待中, 返回 True
        """
        message = wechat_instance.get_message()
        if isinstance(message, EventMessage):
            msgid = message.target + str(message.time)
        else:
            msgid = message.id

        # 在数据库中查找等待中的消息回复
        response = super(ResponseManager, self).get_queryset().filter(
            official_account=official_account
        ).filter(
            msgid=msgid
        ).filter(
            type=Response.TYPE_WAITING
        )
        if response:
            return True
        else:
            return False

    def add_waiting(self, official_account, wechat_instance):
        """
        添加一条新的响应消息记录 (说明该请求正在被执行中)
        :param official_account: 微信公众号实例 (OfficialAccount)
        :param wechat_instance: 微信请求实例 (WechatBasic)
        """
        message = wechat_instance.get_message()
        if isinstance(message, EventMessage):
            msgid = message.target + str(message.time)
        else:
            msgid = message.id

        response = super(ResponseManager, self).create(
            official_account=official_account,
            msgid=msgid,
            target=message.source,
            source=message.target,
            time=int(time()),
            type=Response.TYPE_WAITING,
            pattern=Response.PATTERN_WAITING,
            raw=''
        )
        logger_response.debug('New response created [Detail: %s]' % response.__dict__)
        return response

    def end_waiting(self, official_account, wechat_instance):
        """
        结束一条正在等待的响应消息记录
        :param official_account: 微信公众号实例 (OfficialAccount)
        :param wechat_instance: 微信请求实例 (WechatBasic)
        """
        message = wechat_instance.get_message()
        if isinstance(message, EventMessage):
            msgid = message.target + str(message.time)
        else:
            msgid = message.id

        # 在数据库中查找等待中的消息回复
        response = super(ResponseManager, self).get_queryset().filter(
            official_account=official_account
        ).filter(
            msgid=msgid
        ).filter(
            type=Response.TYPE_WAITING
        )
        if response:
            response[0].delete()


class Response(models.Model):
    """
    微信服务器响应消息记录表
    """
    TYPE_TEXT = 'text'
    TYPE_IMAGE = 'image'
    TYPE_VIDEO = 'video'
    TYPE_VOICE = 'voice'
    TYPE_NEWS = 'news'
    TYPE_MUSIC = 'music'
    TYPE_WAITING = 'waiting'
    TYPE = (
        (TYPE_TEXT, u'文本消息'),
        (TYPE_IMAGE, u'图片消息'),
        (TYPE_VIDEO, u'视频消息'),
        (TYPE_VOICE, u'语音消息'),
        (TYPE_NEWS, u'图文消息'),
        (TYPE_MUSIC, u'音乐消息'),
        (TYPE_WAITING, u'执行中消息'),
    )

    PATTERN_NORMAL = 0
    PATTERN_SERVICE = 1
    PATTERN_SIMULATION = 2
    PATTERN_WAITING = 3
    PATTERN = (
        (PATTERN_NORMAL, u'正常XML返回模式'),
        (PATTERN_SERVICE, u'多客服返回模式'),
        (PATTERN_SIMULATION, u'模拟登陆返回模式'),
        (PATTERN_WAITING, u'执行中消息'),
    )

    official_account = models.ForeignKey(OfficialAccount, verbose_name=u'所属公众号')
    msgid = models.CharField(u'MsgID或FromUserName+CreateTime', max_length=50)
    target = models.CharField(u'目标用户OpenID', max_length=50)
    source = models.CharField(u'来源用户OpenID', max_length=50)
    time = models.IntegerField(u'信息发送时间')
    type = models.CharField(u'信息类型', choices=TYPE, max_length=15)
    pattern = models.IntegerField(u'响应方式', choices=PATTERN)
    raw = models.TextField(u'响应信息原始内容')

    objects = models.Manager()
    manager = ResponseManager()

    class Meta:
        verbose_name = u'微信服务器响应信息'
        verbose_name_plural = u'微信服务器响应信息'
        db_table = 'response'

    def __unicode__(self):
        return self.raw