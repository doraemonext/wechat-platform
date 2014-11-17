# -*- coding: utf-8 -*-

import os
import binascii

from django.db import models

from system.official_account.models import OfficialAccount


class MediaManager(models.Manager):
    def get(self, key):
        """
        获取一个媒体文件
        :param key: 文件唯一 key
        :return: 媒体文件实例 (Media)
        """
        return super(MediaManager, self).get_queryset().get(
            key=key
        )

    def add(self, official_account, file_object, type):
        """
        添加一个新媒体文件
        :param official_account: 所属公众号
        :param file_object: Django File Object
        :param type: 文件类型 (取值见 Media Model)
        :return: 媒体文件实例 (Media)
        """
        filename, extension = os.path.splitext(os.path.basename(file_object.name))

        return super(MediaManager, self).create(
            official_account=official_account,
            type=type,
            filename=filename,
            extension=extension,
            media=file_object,
            size=file_object.size,
        )


class Media(models.Model):
    TYPE_NORMAL = 0
    TYPE_IMAGE = 1
    TYPE_VOICE = 2
    TYPE_MUSIC = 3
    TYPE_VIDEO = 4
    TYPE = (
        (TYPE_NORMAL, u'普通媒体文件'),
        (TYPE_IMAGE, u'图片媒体文件'),
        (TYPE_VOICE, u'语音媒体文件'),
        (TYPE_MUSIC, u'音乐媒体文件'),
        (TYPE_VIDEO, u'视频媒体文件'),
    )

    key = models.CharField(max_length=40, primary_key=True)
    official_account = models.ForeignKey(OfficialAccount, verbose_name=u'所属公众号')
    type = models.IntegerField(u'媒体文件类型', choices=TYPE)
    filename = models.CharField(u'文件名', max_length=50)
    extension = models.CharField(u'文件扩展名', default='', max_length=10)
    media = models.FileField(u'媒体文件', upload_to='media')
    size = models.IntegerField(u'文件大小', default=0)
    created_datetime = models.DateTimeField(u'创建时间', auto_now_add=True)
    modified_datetime = models.DateTimeField(u'最后修改时间', auto_now=True)

    manager = MediaManager()
    objects = models.Manager()

    def __unicode__(self):
        return self.filename + self.extension

    class Meta:
        verbose_name = u'媒体存储'
        verbose_name_plural = u'媒体存储'
        db_table = 'wechat_media'

    @property
    def full_filename(self):
        return self.filename + self.extension

    def save(self, *args, **kwargs):
        """
        在数据库保存过程中新建媒体文件的唯一 key 值
        """
        if not self.key:
            self.key = self.generate_key()
        return super(Media, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()