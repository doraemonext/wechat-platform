# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

from rest_framework import serializers

from lib.tools import validator
from system.official_account.models import OfficialAccount


class OfficialAccountSerializer(serializers.ModelSerializer):
    """
    公众号 序列化类

    """
    iden = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)
    appid = serializers.CharField(required=False)
    appsecret = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    level = serializers.IntegerField(error_messages={
        'required': u'必须选择您的公众号级别',
        'invalid': u'公众号级别非法'
    }, validators=[validator.OfficialAccountLevelValue()])
    name = serializers.CharField(error_messages={
        'required': u'公众号名称不能为空'
    }, validators=[
        validator.MaxValue(u'公众号名称', settings.OFFICIAL_ACCOUNT_NAME_MAX_LEN)
    ])
    email = serializers.EmailField(error_messages={
        'required': u'公众号登录邮箱不能为空',
        'invalid': u'公众号登录邮箱不合法',
    })
    original = serializers.CharField(error_messages={
        'required': u'公众号原始ID不能为空'
    }, validators=[
        validator.MaxValue(u'公众号原始ID', settings.OFFICIAL_ACCOUNT_ORIGINAL_MAX_LEN)
    ])
    wechat = serializers.CharField(error_messages={
        'required': u'微信号不能为空'
    }, validators=[
        validator.MaxValue(u'微信号', settings.OFFICIAL_ACCOUNT_WECHAT_MAX_LEN)
    ])
    introduction = serializers.CharField(required=False)
    address = serializers.CharField(required=False)

    request_url = serializers.SerializerMethodField('get_request_url')
    level_readable = serializers.SerializerMethodField('get_level_readable')

    def get_request_url(self, obj):
        """
        返回公众号的请求接口 URL

        :param obj: 当前 object
        :return: 公众号的请求接口 URL
        """
        view = self.context.get('view')
        if view:
            if view.request.is_secure():
                return 'https://' + view.request.get_host() + reverse('listen:index') + '?iden=' + obj.iden
            else:
                return 'http://' + view.request.get_host() + reverse('listen:index') + '?iden=' + obj.iden
        else:
            return None

    def get_level_readable(self, obj):
        """
        返回公众号等级的具体描述

        :param obj: 当前 object
        :return: 描述公众号等级的字符串
        """
        for level in OfficialAccount.LEVEL:
            if obj.level == level[0]:
                return level[1]

    def validate_appid(self, attrs, source):
        """
        验证appid是否合法

        :param attrs: 属性字典
        :param source: 此处为'appid'
        :return: 属性字典
        """
        appid = attrs[source]
        if attrs.get('level') == OfficialAccount.LEVEL_1:
            if appid:
                del attrs[source]
        elif attrs.get('level') in [OfficialAccount.LEVEL_2, OfficialAccount.LEVEL_3]:
            if not appid:
                raise serializers.ValidationError(u'该公众号级别需要提供App ID')
        return attrs

    def validate_appsecret(self, attrs, source):
        """
        验证appsecret是否合法

        :param attrs: 属性字典
        :param source: 此处为'appsecret'
        :return: 属性字典
        """
        appsecret = attrs[source]
        if attrs.get('level') == OfficialAccount.LEVEL_1:
            if appsecret:
                del attrs[source]
        elif attrs.get('level') in [OfficialAccount.LEVEL_2, OfficialAccount.LEVEL_3]:
            if not appsecret:
                raise serializers.ValidationError(u'该公众号级别需要提供App Secret')
        return attrs

    def validate_username(self, attrs, source):
        """
        验证公众平台用户名是否合法

        :param attrs: 属性字典
        :param source: 此处为'username'
        :return: 属性字典
        """
        username = attrs[source]
        if attrs.get('password'):
            if not username:
                raise serializers.ValidationError(u'当提供公众平台密码后需要输入公众平台用户名')
        return attrs

    def validate_password(self, attrs, source):
        """
        验证公众平台密码是否合法

        :param attrs: 属性字典
        :param source: 此处为'password'
        :return: 属性字典
        """
        password = attrs[source]
        if attrs.get('username'):
            if not password:
                raise serializers.ValidationError(u'当提供公众平台用户名后需要输入公众平台密码')
        return attrs

    def save(self, **kwargs):
        """
        重载默认的save方法，使得在POST请求新建公众号时可以调用OfficialAccount manager中的方法

        :return: 保存好的object
        """
        view = self.context.get('view')

        if view and view.request.method == 'POST':
            self.object = OfficialAccount.manager.add(
                level=self.object.level,
                name=self.object.name,
                email=self.object.email,
                original=self.object.original,
                wechat=self.object.wechat,
                introduction=self.object.introduction,
                address=self.object.address,
                appid=self.object.appid,
                appsecret=self.object.appsecret,
                username=self.object.username,
                password=self.object.password
            )
            return self.object
        else:
            return super(OfficialAccountSerializer, self).save(**kwargs)

    class Meta:
        model = OfficialAccount
        fields = ('id', 'iden', 'token', 'appid', 'appsecret', 'username', 'password', 'level',
                  'name', 'email', 'original', 'wechat', 'introduction', 'address',
                  'request_url', 'level_readable')