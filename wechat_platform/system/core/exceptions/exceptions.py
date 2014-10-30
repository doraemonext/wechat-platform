# -*- coding: utf-8 -*-


class WechatException(Exception):
    pass


class WechatInstanceException(WechatException):
    pass


class WechatRequestRepeatException(WechatException):
    pass


class PluginException(Exception):
    pass


class PluginLoadError(PluginException):
    pass