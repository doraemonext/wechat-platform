# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from rest_framework import serializers

from lib.tools import validator
from system.library.music.models import LibraryMusic
from system.media.models import Media


class LibraryMusicSerializer(serializers.ModelSerializer):
    """
    系统素材库 - 音乐库 序列化类
    """
    music = serializers.PrimaryKeyRelatedField(error_messages={
        'required': '必须上传普通音乐文件',
    })
    hq_music = serializers.PrimaryKeyRelatedField(required=False)
    thumb = serializers.PrimaryKeyRelatedField(required=False)
    thumb_url = serializers.SerializerMethodField('get_thumb_url')
    music_detail = serializers.SerializerMethodField('get_music_detail')
    hq_music_detail = serializers.SerializerMethodField('get_hq_music_detail')
    thumb_detail = serializers.SerializerMethodField('get_thumb_detail')

    def get_thumb_url(self, obj):
        if obj.thumb:
            return reverse('filetranslator:download', kwargs={'key': obj.thumb.pk})
        else:
            return None

    def get_music_detail(self, obj):
        if obj.music:
            return obj.music.__dict__
        else:
            return {}

    def get_hq_music_detail(self, obj):
        if obj.hq_music:
            return obj.hq_music.__dict__
        else:
            return {}

    def get_thumb_detail(self, obj):
        if obj.thumb:
            return obj.thumb.__dict__
        else:
            return {}

    def save(self, **kwargs):
        """
        重载默认的 save 方法，使得在 POST 请求新建公众号时可以调用 LibraryMusic manager 中的方法
        :return: 保存好的 object
        """
        view = self.context.get('view')

        if view and view.request.method == 'POST':
            self.object = LibraryMusic.manager.add(
                official_account=self.object.official_account,
                plugin_iden=self.object.plugin_iden,
                title=self.object.title,
                description=self.object.description,
                music_url=self.object.music_url,
                hq_music_url=self.object.hq_music_url,
                thumb_media_id=self.object.thumb_media_id,
                music=self.object.music,
                hq_music=self.object.hq_music,
                thumb=self.object.thumb,
            )
            return self.object
        else:
            return super(LibraryMusicSerializer, self).save(**kwargs)

    class Meta:
        model = LibraryMusic
        fields = ('id', 'official_account', 'plugin_iden', 'title', 'description', 'music_url', 'hq_music_url',
                  'thumb_url', 'thumb_media_id', 'music', 'hq_music', 'thumb', 'music_detail', 'hq_music_detail', 'thumb_detail')