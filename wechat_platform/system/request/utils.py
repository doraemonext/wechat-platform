# -*- coding: utf-8 -*-

from system.core.exceptions import WechatException


class RequestException(WechatException):
    pass


class RequestRepeatException(RequestException):
    pass