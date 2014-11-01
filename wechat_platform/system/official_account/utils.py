# -*- coding: utf-8 -*-

from system.core.exceptions import WechatException


class OfficialAccountException(WechatException):
    pass


class OfficialAccountIncomplete(OfficialAccountException):
    """
    公众号自身信息不完整
    """
    pass


class OfficialAccountIncorrect(OfficialAccountException):
    """
    公众号自身信息不正确
    """
    pass