# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import Group

from rest_framework import serializers

from lib.tools import validator


class GroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(error_messages={
        'required': u'必须填写用户组名'
    }, validators=[
        validator.MaxValue(u'用户组名', settings.GROUP_NAME_MAX_LEN)
    ])
    #    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'name')