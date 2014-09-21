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
    permissions = PermissionSerializer()

    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions')


class MemberSerializer(serializers.ModelSerializer):
    groups = GroupSerializer()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'nickname', 'email', 'groups', 'date_joined')