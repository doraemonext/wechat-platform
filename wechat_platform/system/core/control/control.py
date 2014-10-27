# -*- coding: utf-8 -*-

from django.http.response import HttpResponse

from wechat_sdk.context.framework.django import DatabaseContextStore
from wechat_sdk.messages import EventMessage


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
        self.official_account = official_account  # 公众号实例
        self.wechat = wechat_instance  # 微信请求
        self.message = self.wechat.get_message()  # 微信消息
        self.context = DatabaseContextStore(openid=self.message.source)  # 微信上下文对话

    @property
    def response(self):
        # 保存所有上下文对话到数据库中
        self.context.save()

        return HttpResponse('hello')
