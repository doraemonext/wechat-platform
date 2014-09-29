# -*- coding: utf-8 -*-

import re

from django.core.exceptions import ValidationError

from system.official_account.models import OfficialAccount


class MinValue(object):
    """
    最小长度验证
    """
    def __init__(self, name, length):
        self.name = name
        self.length = length

    def __call__(self, value, *args, **kwargs):
        if len(value) < self.length:
            raise ValidationError(u'%s最小长度为%d个字符' % (self.name, self.length))


class MaxValue(object):
    """
    最大长度验证
    """
    def __init__(self, name, length):
        self.name = name
        self.length = length

    def __call__(self, value, *args, **kwargs):
        if len(value) > self.length:
            raise ValidationError(u'%s最大长度为%d个字符' % (self.name, self.length))


class SafeValue(object):
    """
    安全字符验证

    仅允许包含汉字、数字、字母、下划线及短横线
    """
    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        if not re.search(u'^[_a-zA-Z0-9\u4e00-\u9fa5\-]+$', value):
            raise ValidationError(u'%s包含非法字符' % self.name)


class OfficialAccountLevelValue(object):
    """
    公众号级别验证

    仅允许在 OfficialAccount Model 中存在的级别
    """
    def __call__(self, value, *args, **kwargs):
        valid = False
        for level in OfficialAccount.LEVEL:
            if value == level[0]:
                valid = True
                break
        if not valid:
            raise ValidationError(u'公众号级别非法')