# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model

from rest_framework import serializers

from lib.tools import validator


class MemberSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField('get_nickname')
    group = serializers.SerializerMethodField('get_group')

    def get_nickname(self, obj):
        """
        Just for test
        :param obj:
        :return:
        """
        return obj.username

    def get_group(self, obj):
        return u'超级管理员'

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'nickname', 'email', 'group', 'date_joined')