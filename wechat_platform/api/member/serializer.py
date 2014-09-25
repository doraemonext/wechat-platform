# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from lib.tools import validator


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'codename')


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions')


class MemberSerializer(serializers.ModelSerializer):
    error_messages = {
        'duplicate': u'该用户已存在，请换一个新的用户名',
    }

    username = serializers.CharField(error_messages={
        'required': u'用户名不能为空'
    }, validators=[
        validator.MinValue(u'用户名', settings.USERNAME_MIN_LEN),
        validator.MaxValue(u'用户名', settings.USERNAME_MAX_LEN),
        validator.SafeValue(u'用户名'),
    ])
    nickname = serializers.CharField(error_messages={'required': u'昵称不能为空'}, validators=[
        validator.MinValue(u'昵称', settings.NICKNAME_MIN_LEN),
        validator.MaxValue(u'昵称', settings.NICKNAME_MAX_LEN),
        validator.SafeValue(u'昵称'),
    ])
    email = serializers.EmailField(error_messages={
        'required': u'电子邮件不能为空',
        'invalid': u'电子邮件地址不合法',
    })
    password = serializers.CharField(write_only=True, error_messages={'required': u'密码不能为空'}, validators=[
        validator.MinValue(u'密码', settings.PASSWORD_MIN_LEN),
        validator.MaxValue(u'密码', settings.PASSWORD_MAX_LEN),
    ])
    groups = GroupSerializer(many=True, read_only=True)

    def validate_username(self, attrs, source):
        username = attrs[source]
        if self.context.get('view') and self.context['view'].request.method == 'POST':
            try:
                get_user_model().objects.get(username=username)
            except ObjectDoesNotExist:
                return attrs
            raise serializers.ValidationError(
                u'该用户已存在，请换一个新的用户名',
                code='duplicate',
            )
        return attrs

    def save(self, **kwargs):
        view = self.context.get('view')

        if view and view.request.method == 'POST':
            return get_user_model().objects.create_user(
                username=self.object.username,
                email=self.object.email,
                nickname=self.object.nickname,
                password=self.object.password
            )
        else:
            return super(MemberSerializer, self).save(**kwargs)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'nickname', 'email', 'password', 'groups', 'date_joined')
        read_only_fields = ('date_joined', )