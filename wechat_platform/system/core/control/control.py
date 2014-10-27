# -*- coding: utf-8 -*-

from wechat_sdk.context.framework.django import DatabaseContextStore


class ControlCenter(object):
    """
    微信控制中心类
    """
    def __init__(self, official_account, wechat_instance):
        """
        控制中心初始化
        :param official_account: 公众号实例 (OfficialAccount)
        :param wechat_instance: 微信请求实例 (WechatBasic)
        """
        self.official_account = official_account
        self.wechat = wechat_instance
        self.context = DatabaseContextStore(self.wechat.get_message().source)

    @property
    def response(self):
        pass