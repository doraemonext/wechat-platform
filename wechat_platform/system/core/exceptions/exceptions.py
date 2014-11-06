# -*- coding: utf-8 -*-


class WechatException(Exception):
    pass


class WechatCriticalException(WechatException):
    """
    严重系统错误, 无法继续运行
    """
    pass


class WechatInstanceException(WechatException):
    pass


# asdfasdf