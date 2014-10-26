# -*- coding: utf-8 -*-

import time
from hashlib import sha1

from django.test import TestCase
from django.test.client import Client

from lib.tools.random import make_random_string, make_unique_random_string
from system.official_account.models import OfficialAccount


class WechatTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def make_verify_parameter(self, token):
        """
        生成微信请求的验证参数
        :param token: 微信 Token
        :return:
        """
        timestamp = str(int(time.time()))
        nonce = make_random_string(13)

        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = ''.join(tmp_list)
        signature = sha1(tmp_str).hexdigest()

        return signature, timestamp, nonce

    def make_official_account(self, level, name='test_name', email='test@test.com', original='gh_1234567',
                              wechat='test', introduction=None, address=None, appid=None, appsecret=None,
                              username=None, password=None, is_advanced=False, token=None):
        """
        生成一个公众号
        :param level: 公众号级别
        :param name: 公众号名称
        :param email: 公众号登录邮箱
        :param original: 公众号原始ID
        :param wechat: 微信号
        :param introduction: 公众号介绍
        :param address: 所在地址
        :param appid: 微信 App ID, 认证订阅号/普通服务号/认证服务号必填
        :param appsecret: 微信 App Secret, 认证订阅号/普通服务号/认证服务号必填
        :param username: 公众平台用户名
        :param password: 公众平台密码
        :param is_advanced: 是否开启高级支持
        :param token: 微信 Token, 如不传入将自动生成
        """
        return OfficialAccount.manager.add(level, name, email, original, wechat, introduction, address,
                                           appid, appsecret, username, password, is_advanced, token)