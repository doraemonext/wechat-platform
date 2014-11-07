# -*- coding: utf-8 -*-

from system.core.exceptions import WechatException


class RepeatRequest(WechatException):
    """
    重复请求且已有数据可以直接回复
    """
    def __init__(self, response):
        self.response = response