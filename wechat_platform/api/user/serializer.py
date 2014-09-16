# -*- coding: utf-8 -*-

from rest_framework import serializers

from lib.tools import validator


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(error_messages={'required': u'用户名不能为空'}, validators=[
        validator.MinValue(u'用户名', 2),
        validator.MaxValue(u'用户名', 32),
        validator.SafeValue(u'用户名'),
    ])
    password = serializers.CharField(max_length=128, error_messages={'required': u'密码不能为空'}, validators=[
        validator.MinValue(u'密码', 4),
        validator.MaxValue(u'密码', 64),
    ])
    next = serializers.CharField(max_length=255, required=False)
