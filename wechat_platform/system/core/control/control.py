# -*- coding: utf-8 -*-

from wechat_sdk.context.framework.django import DatabaseContextStore


class ControlCenter(object):
    def __init__(self, official_account, wechat_instance):
        self.official_account = official_account
        self.wechat = wechat_instance
        self.context = DatabaseContextStore(self.wechat.get_message().target)

    @property
    def response(self):
        return 'hello'