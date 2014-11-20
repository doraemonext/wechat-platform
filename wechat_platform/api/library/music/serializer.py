# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

from rest_framework import serializers

from lib.tools import validator
from system.library.music.models import LibraryMusic


class LibraryMusicSerializer(serializers.ModelSerializer):
    """
    系统素材库 - 音乐库 序列化类
    """
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
                thumb_media=self.object.thumb_media,
            )
            return self.object
        else:
            return super(LibraryMusicSerializer, self).save(**kwargs)

    class Meta:
        model = LibraryMusic
        fields = ('id', 'official_account', 'plugin_iden', 'title', 'description', 'music_url', 'hq_music_url',
                  'thumb_media_id', 'music', 'hq_music', 'thumb')