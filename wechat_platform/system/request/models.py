# -*- coding: utf-8 -*-

from django.db import models
from django.db import IntegrityError

from system.core.exceptions import WechatInstanceException, WechatRequestRepeatException
from system.official_account.models import OfficialAccount


class RequestMessageManager(models.Manager):
    """
    微信服务器请求记录表 Manager
    """
    def is_repeat(self, official_account, wechat_instance=None, msgid=None):
        """
        根据msgid判断改请求是否重复

        wechat_instance和msgid二选一传入即可
        :param official_account: 所属公众号
        :param wechat_instance: wechat实例
        :param msgid: 消息ID
        :return: 当重复时返回True
        """
        if wechat_instance is not None:
            msgid = wechat_instance.get_message().id
        return super(RequestMessageManager, self).get_queryset().filter(
            official_account=official_account
        ).filter(
            pk=msgid
        ).exists()

    def add(self, official_account, wechat_instance):
        """
        根据wechat实例自动添加事件
        :param official_account: 所属公众号
        :param wechat_instance: Wechat 实例 (WechatBasic)
        :raise WechatInstanceException: 当传入Wechat实例非法时抛出此异常
        """
        message = wechat_instance.get_message()

        if message.type == 'text':
            return self.add_text(
                official_account=official_account,
                msgid=message.id,
                target=message.target,
                source=message.source,
                time=message.time,
                raw=message.raw,
                content=message.content
            )
        elif message.type == 'image':
            return self.add_image(
                official_account=official_account,
                msgid=message.id,
                target=message.target,
                source=message.source,
                time=message.time,
                raw=message.raw,
                picurl=message.picurl
            )
        else:
            raise WechatInstanceException()

    def add_text(self, official_account, msgid, target, source, time, raw, content):
        """
        添加文本消息请求

        :param official_account: 所属公众号
        :param msgid: 消息ID
        :param target: 目标用户OpenID
        :param source: 来源用户OpenID
        :param time: 信息发送时间
        :param raw: 信息的原始XML格式
        :param content: 文本消息内容
        """
        try:
            return super(RequestMessageManager, self).create(
                official_account=official_account,
                msgid=msgid,
                target=target,
                source=source,
                time=time,
                raw=raw,
                type=RequestMessage.TYPE_TEXT,
                text_content=content
            )
        except IntegrityError, e:
            raise WechatRequestRepeatException(e)

    def add_image(self, official_account, msgid, target, source, time, raw, picurl):
        """
        添加图片消息请求

        :param official_account: 所属公众号
        :param msgid: 消息ID
        :param target: 目标用户OpenID
        :param source: 来源用户OpenID
        :param time: 信息发送时间
        :param raw: 信息的原始XML格式
        :param picurl: 图片链接
        """
        try:
            return super(RequestMessageManager, self).create(
                official_account=official_account,
                msgid=msgid,
                target=target,
                source=source,
                time=time,
                raw=raw,
                type=RequestMessage.TYPE_IMAGE,
                image_picurl=picurl
            )
        except IntegrityError, e:
            raise WechatRequestRepeatException(e)


class RequestMessage(models.Model):
    """
    微信服务器请求消息记录表
    """
    TYPE_TEXT = 'text'
    TYPE_IMAGE = 'image'
    TYPE_VIDEO = 'video'
    TYPE_LINK = 'link'
    TYPE_LOCATION = 'location'
    TYPE_VOICE = 'voice'
    TYPE = (
        (TYPE_TEXT, u'文本消息'),
        (TYPE_IMAGE, u'图片消息'),
        (TYPE_VIDEO, u'视频消息'),
        (TYPE_LINK, u'链接消息'),
        (TYPE_LOCATION, u'地理位置消息'),
        (TYPE_VOICE, u'语音消息'),
    )

    official_account = models.ForeignKey(OfficialAccount, verbose_name=u'所属公众号')
    msgid = models.BigIntegerField(u'消息ID', primary_key=True)
    target = models.CharField(u'目标用户OpenID', max_length=50)
    source = models.CharField(u'来源用户OpenID', max_length=50)
    time = models.IntegerField(u'信息发送时间')
    raw = models.TextField(u'信息原始XML内容')
    type = models.CharField(u'信息类型', choices=TYPE, max_length=15)
    text_content = models.TextField(u'文本消息-信息内容', blank=True, null=True)
    image_picurl = models.URLField(u'图片消息-图片网址', blank=True, null=True)
    video_media_id = models.CharField(u'视频消息-媒体ID', max_length=50, blank=True, null=True)
    video_thumb_media_id = models.CharField(u'视频消息-缩略图媒体ID', max_length=50, blank=True, null=True)
    link_title = models.CharField(u'链接消息-标题', max_length=80, blank=True, null=True)
    link_description = models.TextField(u'链接消息-描述', blank=True, null=True)
    link_url = models.URLField(u'链接消息-链接', blank=True, null=True)
    location_x = models.FloatField(u'地理位置消息-纬度', blank=True, null=True)
    location_y = models.FloatField(u'地理位置消息-经度', blank=True, null=True)
    location_scale = models.FloatField(u'地理位置消息-缩放大小', blank=True, null=True)
    location_label = models.CharField(u'地理位置消息-位置信息', max_length=80, blank=True, null=True)
    voice_media_id = models.CharField(u'语音消息-媒体ID', max_length=50, blank=True, null=True)
    voice_format = models.CharField(u'语音消息-声音格式', max_length=20, blank=True, null=True)
    voice_recognition = models.TextField(u'语音消息-识别结果', blank=True, null=True)

    objects = models.Manager()
    manager = RequestMessageManager()

    class Meta:
        verbose_name = u'微信服务器请求消息'
        verbose_name_plural = u'微信服务器请求消息'
        db_table = 'request_message'

    def __unicode__(self):
        return self.raw


class RequestEventManager(models.Manager):
    """
    微信服务器请求事件记录表 Manager
    """
    def is_repeat(self, official_account, wechat_instance=None, source=None, time=None):
        """
        根据source+time判断改请求是否重复 (微信官方推荐方式)

        wechat实例和source/time二选一传入即可
        :param official_account: 所属公众号
        :param wechat_instance: wechat实例
        :param source: 来源用户OpenID
        :param time: 信息发送时间
        :return: 当重复时返回True
        """
        if wechat_instance is not None:
            source = wechat_instance.get_message().source
            time = wechat_instance.get_message().time
        return super(RequestEventManager, self).get_queryset().filter(
            official_account=official_account
        ).filter(
            pk=source+str(time)
        ).exists()

    def add(self, official_account, wechat_instance):
        """
        根据wechat实例自动添加事件
        :param official_account: 所属公众号
        :param wechat_instance: Wechat 实例 (WechatBasic), 请保证传入实例为的消息类型为 EventMessage
        :raise WechatInstanceException: 当传入Wechat实例非法时抛出此异常
        """
        message = wechat_instance.get_message()
        if message.type == 'subscribe':
            return self.add_subscribe(
                official_account=official_account,
                target=message.target,
                source=message.source,
                time=message.time,
                raw=message.raw
            )
        elif message.type == 'unsubscribe':
            return self.add_unsubscribe(
                official_account=official_account,
                target=message.target,
                source=message.source,
                time=message.time,
                raw=message.raw
            )
        elif message.type == 'click':
            return self.add_click(
                official_account=official_account,
                target=message.target,
                source=message.source,
                time=message.time,
                key=message.key,
                raw=message.raw
            )
        elif message.type == 'location':
            return self.add_location(
                official_account=official_account,
                target=message.target,
                source=message.source,
                time=message.time,
                raw=message.raw,
                latitude=message.latitude,
                longitude=message.longitude,
                precision=message.precision
            )
        else:
            raise WechatInstanceException()

    def add_subscribe(self, official_account, target, source, time, raw):
        """
        添加订阅请求记录
        :param official_account: 所属公众号
        :param target: 目标用户OpenID
        :param source: 来源用户OpenID
        :param time: 信息发送时间
        :param raw: 原始XML
        """
        try:
            return super(RequestEventManager, self).create(
                official_account=official_account,
                eventid=source+str(time),
                target=target,
                source=source,
                time=time,
                type=RequestEvent.TYPE_SUBSCRIBE,
                raw=raw
            )
        except IntegrityError, e:
            raise WechatRequestRepeatException(e)

    def add_unsubscribe(self, official_account, target, source, time, raw):
        """
        添加取消订阅请求记录
        :param official_account: 所属公众号
        :param target: 目标用户OpenID
        :param source: 来源用户OpenID
        :param time: 信息发送时间
        :param raw: 原始XML
        """
        try:
            return super(RequestEventManager, self).create(
                official_account=official_account,
                eventid=source+str(time),
                target=target,
                source=source,
                time=time,
                type=RequestEvent.TYPE_UNSUBSCRIBE,
                raw=raw
            )
        except IntegrityError, e:
            raise WechatRequestRepeatException(e)

    def add_click(self, official_account, target, source, time, raw, key):
        """
        添加自定义菜单点击事件
        :param official_account: 所属公众号
        :param target: 目标用户OpenID
        :param source: 来源用户OpenID
        :param time: 信息发送时间
        :param raw: 原始XML
        :param key: 事件KEY值
        """
        try:
            return super(RequestEventManager, self).create(
                official_account=official_account,
                eventid=source+str(time),
                target=target,
                source=source,
                time=time,
                type=RequestEvent.TYPE_CLICK,
                raw=raw,
                key=key
            )
        except IntegrityError, e:
            raise WechatRequestRepeatException(e)

    def add_location(self, official_account, target, source, time, raw, latitude, longitude, precision):
        """
        添加上报地理位置事件
        :param official_account: 所属公众号
        :param target: 目标用户OpenID
        :param source: 来源用户OpenID
        :param time: 信息发送时间
        :param raw: 原始XML
        :param latitude: 纬度
        :param longitude: 经度
        :param precision: 精度
        """
        try:
            return super(RequestEventManager, self).create(
                official_account=official_account,
                eventid=source+str(time),
                target=target,
                source=source,
                time=time,
                type=RequestEvent.TYPE_LOCATION,
                raw=raw,
                latitude=latitude,
                longitude=longitude,
                precision=precision
            )
        except IntegrityError, e:
            raise WechatRequestRepeatException(e)


class RequestEvent(models.Model):
    """
    微信服务器请求事件记录表
    """
    TYPE_SUBSCRIBE = 'subscribe'
    TYPE_UNSUBSCRIBE = 'unsubscribe'
    TYPE_CLICK = 'click'
    TYPE_LOCATION = 'location'
    TYPE = (
        (TYPE_SUBSCRIBE, u'订阅事件'),
        (TYPE_UNSUBSCRIBE, u'取消订阅事件'),
        (TYPE_CLICK, u'点击事件'),
        (TYPE_LOCATION, u'地理位置事件'),
    )

    official_account = models.ForeignKey(OfficialAccount, verbose_name=u'所属公众号')
    eventid = models.CharField(u'事件ID', max_length=50, primary_key=True)
    target = models.CharField(u'目标用户OpenID', max_length=50)
    source = models.CharField(u'来源用户OpenID', max_length=50)
    time = models.IntegerField(u'信息发送时间')
    raw = models.TextField(u'信息原始XML内容')
    type = models.CharField(u'事件类型', choices=TYPE, max_length=15, blank=True, null=True)
    key = models.TextField(u'事件key值', blank=True, null=True)
    latitude = models.FloatField(u'地理位置事件-纬度', blank=True, null=True)
    longitude = models.FloatField(u'地理位置事件-经度', blank=True, null=True)
    precision = models.FloatField(u'地理位置事件-精度', blank=True, null=True)

    objects = models.Manager()
    manager = RequestEventManager()

    class Meta:
        verbose_name = u'微信服务器请求事件'
        verbose_name_plural = u'微信服务器请求事件'
        db_table = 'request_event'

    def __unicode__(self):
        return self.raw