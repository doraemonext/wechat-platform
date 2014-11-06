# -*- coding: utf-8 -*-

from system.core.exceptions import WechatException


class PluginException(Exception):
    pass


class PluginDoesNotExist(PluginException):
    pass


class PluginLoadError(PluginException):
    pass


class PluginRuntimeError(PluginException):
    pass


class PluginResponseError(PluginException):
    pass