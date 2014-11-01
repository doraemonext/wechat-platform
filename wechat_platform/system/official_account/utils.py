# -*- coding: utf-8 -*-

from system.core.exceptions import WechatException


class OfficialAccountIncomplete(WechatException):
    """
    公众号自身信息不完整
    """
    pass


class OfficialAccountIncorrect(WechatException):
    """
    公众号自身信息不正确
    """
    pass