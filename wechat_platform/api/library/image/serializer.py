# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from rest_framework import serializers

from lib.tools import validator
from system.library.image.models import LibraryImage
from system.media.models import Media


class LibraryImageSerializer(serializers.ModelSerializer):
    """
    系统素材库 - 图片库 序列化类
    """
    image = serializers.PrimaryKeyRelatedField(error_messages={
        'required': u'必须上传图片文件',
    })
    image_url = serializers.SerializerMethodField('get_image_url')
    image_detail = serializers.SerializerMethodField('get_image_detail')

    def get_image_url(self, obj):
        if obj.image:
            return reverse('filetranslator:download', kwargs={'key': obj.image.pk})
        else:
            return None

    def get_image_detail(self, obj):
        if obj.image:
            return obj.image.__dict__
        else:
            return {}

    def validate_image(self, attrs, source):
        image = attrs.get(source)
        if not image:
            raise serializers.ValidationError(u'必须上传图片文件')
        return attrs

    def save(self, **kwargs):
        """
        重载默认的 save 方法，使得在 POST 请求新建公众号时可以调用 LibraryMusic manager 中的方法
        :return: 保存好的 object
        """
        view = self.context.get('view')

        if view and view.request.method == 'POST':
            self.object = LibraryImage.manager.add(
                official_account=self.object.official_account,
                plugin_iden=self.object.plugin_iden,
                image=self.object.image,
            )
            return self.object
        else:
            return super(LibraryImageSerializer, self).save(**kwargs)

    class Meta:
        model = LibraryImage
        fields = ('id', 'official_account', 'plugin_iden', 'image', 'image_url', 'image_detail', 'fid', 'media_id')
        read_only_fields = ('fid', 'media_id')