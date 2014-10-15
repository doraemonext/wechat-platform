# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import Group, Permission

from rest_framework import serializers

from lib.tools import validator
from system.permission.models import CustomPermission


class PermissionSerializer(serializers.ModelSerializer):
    def valid_codename(self, codename):
        view = self.context['view']
        if not view:
            return False

        if view.request.user.is_superuser:
            return True
        else:
            return False

    @property
    def data(self):
        if self._data is None:
            self._data = dict()
            for item in self.object:
                group_name = item.codename.split('_', 1)[1]
                if self._data.get(group_name):
                    operator = item.codename.split('_', 1)[0]
                    self._data[group_name]['sub'][operator] = {
                        'codename': item.codename,
                        'valid': self.valid_codename(item.codename)
                    }
                else:
                    self._data[group_name] = {
                        'name_readable': item.codename,
                        'sub': {
                            item.codename.split('_', 1)[0]: {
                                'codename': item.codename,
                                'valid': self.valid_codename(item.codename)
                            }
                        }
                    }

        return self._data

    class Meta:
        model = Permission
        fields = ('id', 'name', 'codename')


class GroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(error_messages={
        'required': u'必须填写用户组名'
    }, validators=[
        validator.MaxValue(u'用户组名', settings.GROUP_NAME_MAX_LEN)
    ])
    permissions = serializers.SerializerMethodField('get_group_permissions')

    def get_group_permissions(self, obj):
        permissions = PermissionSerializer(CustomPermission.manager.get(), many=True, context=self.context)
        return permissions.data

    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions')