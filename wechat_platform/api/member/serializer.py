# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

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
    groups = GroupSerializer(many=True, read_only=True)

    def save(self, **kwargs):
        return get_user_model().objects.create_user(
            username=self.object.username,
            email=self.object.email,
            nickname=self.object.nickname,
            password=self.object.password
        )

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'nickname', 'email', 'groups', 'date_joined')
        read_only_fields = ('date_joined', )