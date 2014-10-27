# -*- coding: utf-8 -*-

from django.db import models


class Request(models.Model):
    """
    微信服务器请求记录表
    """
    TYPE_TEXT = 'text'
    TYPE_IMAGE = 'image'
    TYPE_VIDEO = 'video'
    TYPE_LINK = 'link'
    TYPE_LOCATION = 'location'
    TYPE_EVENT = 'event'
    TYPE_VOICE = 'voice'
    TYPE = (
        (TYPE_TEXT, u'文本消息'),
        (TYPE_IMAGE, u'图片消息'),
        (TYPE_VIDEO, u'视频消息'),
        (TYPE_LINK, u'链接消息'),
        (TYPE_LOCATION, u'地理位置消息'),
        (TYPE_EVENT, u'事件消息'),
        (TYPE_VOICE, u'语音消息'),
    )

    EVENT_TYPE_SUBSCRIBE = 'subscribe'
    EVENT_TYPE_UNSUBSCRIBE = 'unsubscribe'
    EVENT_TYPE_CLICK = 'click'
    EVENT_TYPE_LOCATION = 'location'
    EVENT_TYPE = (
        (EVENT_TYPE_SUBSCRIBE, u'订阅事件'),
        (EVENT_TYPE_UNSUBSCRIBE, u'取消订阅事件'),
        (EVENT_TYPE_CLICK, u'点击事件'),
        (EVENT_TYPE_LOCATION, u'地理位置事件'),
    )

    msgid = models.CharField(u'消息ID', max_length=25, primary_key=True)
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
    event_type = models.CharField(u'事件类型', choices=EVENT_TYPE, max_length=15, blank=True, null=True)
    event_key = models.TextField(u'事件key值', blank=True, null=True)
    event_latitude = models.FloatField(u'地理位置事件-纬度', blank=True, null=True)
    event_longitude = models.FloatField(u'地理位置事件-经度', blank=True, null=True)
    event_precision = models.FloatField(u'地理位置事件-精度', blank=True, null=True)
    voice_media_id = models.CharField(u'语音消息-媒体ID', max_length=50, blank=True, null=True)
    voice_format = models.CharField(u'语音消息-声音格式', max_length=20, blank=True, null=True)
    voice_recognition = models.TextField(u'语音消息-识别结果', blank=True, null=True)

    class Meta:
        verbose_name = u'微信服务器请求'
        verbose_name_plural = u'微信服务器请求'
        db_table = 'wechat_request'

    def __unicode__(self):
        return self.raw