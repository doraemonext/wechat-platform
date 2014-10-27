# -*- coding: utf-8 -*-

from django.db import models

from system.core.exceptions import WechatInstanceException


class RequestMessageManager(models.Manager):
    """
    微信服务器请求记录表 Manager
    """
    def add(self, wechat_instance):
        message = wechat_instance.get_message()

        if message.type == 'text':
            return self.add_text(
                msgid=message.id,
                target=message.target,
                source=message.source,
                time=message.time,
                raw=message.raw,
                content=message.content
            )
        elif message.type == 'image':
            return self.add_image(
                msgid=message.id,
                target=message.target,
                source=message.source,
                time=message.time,
                raw=message.raw,
                picurl=message.picurl
            )
        else:
            raise WechatInstanceException()

    def add_text(self, msgid, target, source, time, raw, content):
        """
        添加文本消息请求

        :param msgid: 消息ID
        :param target: 目标用户OpenID
        :param source: 来源用户OpenID
        :param time: 信息发送时间
        :param raw: 信息的原始XML格式
        :param content: 文本消息内容
        """
        return super(RequestMessageManager, self).create(
            msgid=msgid,
            target=target,
            source=source,
            time=time,
            raw=raw,
            type=RequestMessage.TYPE_TEXT,
            text_content=content
        )

    def add_image(self, msgid, target, source, time, raw, picurl):
        """
        添加图片消息请求

        :param msgid: 消息ID
        :param target: 目标用户OpenID
        :param source: 来源用户OpenID
        :param time: 信息发送时间
        :param raw: 信息的原始XML格式
        :param picurl: 图片链接
        """
        return super(RequestMessageManager, self).create(
            msgid=msgid,
            target=target,
            source=source,
            time=time,
            raw=raw,
            type=RequestMessage.TYPE_IMAGE,
            image_picurl=picurl
        )


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
    pass


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

    eventid = models.CharField(u'事件ID', max_length=50, primary_key=True)
    target = models.CharField(u'目标用户OpenID', max_length=50)
    source = models.CharField(u'来源用户OpenID', max_length=50)
    time = models.IntegerField(u'信息发送时间')
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