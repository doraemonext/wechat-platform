# -*- coding: utf-8 -*-

import os
import filecmp

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

from rest_framework import serializers

from lib.tools import validator
from system.media.models import Media


class MediaSerializer(serializers.ModelSerializer):
    """
    系统媒体文件 序列化类 (仅用于单个媒体文件的 获取(GET)/更新(PATCH)/删除(DELETE))
    """
    def validate_media(self, attrs, source):
        media = attrs.get(source)
        if media:
            filename, extension = os.path.splitext(os.path.basename(media.name))
            if not filename or not extension:
                raise serializers.ValidationError(u'文件必须拥有文件名及扩展名')
        return attrs

    def restore_object(self, attrs, instance=None):
        """
        该函数根据是否更新了媒体文件实体来修改对应的文件名和扩展名的值

        如果更新了媒体文件实体, 则文件名及扩展名取对应的新的媒体文件的文件名和扩展名
        如果没有更新媒体文件实体, 则根据用户提交的文件名和扩展名数据更新该媒体文件的文件名和扩展名
        """
        instance = super(MediaSerializer, self).restore_object(attrs=attrs, instance=instance)
        origin_instance = Media.manager.get(key=instance.key)
        if not instance.media.read() == origin_instance.media.read():
            instance.filename, instance.extension = os.path.splitext(os.path.basename(instance.media.name))
        return instance

    class Meta:
        model = Media
        fields = ('key', 'official_account', 'type', 'filename', 'extension', 'media', 'size',
                  'created_datetime', 'modified_datetime')
        read_only_fields = ('key', 'official_account', 'size', 'created_datetime', 'modified_datetime')


class MediaUploadSerializer(serializers.ModelSerializer):
    """
    系统媒体文件上传 序列化类 (仅用于媒体文件的新建(POST))
    """
    official_account = serializers.PrimaryKeyRelatedField()
    media = serializers.FileField()  # 以文件形式上传
    type = serializers.IntegerField()

    def validate_media(self, attrs, source):
        media = attrs.get(source)
        if media:
            filename, extension = os.path.splitext(os.path.basename(media.name))
            if not filename or not extension:
                raise serializers.ValidationError(u'文件必须拥有文件名及扩展名')
        return attrs

    def save(self, **kwargs):
        """
        重载默认的save方法，使得在POST请求上传媒体文件时可以调用Media manager中的方法

        :return: 保存好的object
        """
        view = self.context.get('view')

        if view and view.request.method == 'POST':
            self.object = Media.manager.add(
                official_account=self.object.official_account,
                type=self.object.type,
                file_object=self.object.media,
            )
            return self.object
        else:
            return super(MediaUploadSerializer, self).save(**kwargs)

    class Meta:
        model = Media
        fields = ('key', 'official_account', 'type', 'filename', 'extension', 'media', 'size',
                  'created_datetime', 'modified_datetime')
        read_only_fields = ('key', 'filename', 'extension', 'size', 'created_datetime', 'modified_datetime')