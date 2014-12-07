# -*- coding: utf-8 -*-

import time
from hashlib import sha1

from django.test import TestCase
from django.test.client import Client, RequestFactory

from lib.tools.rand import make_random_string, make_unique_random_string
from system.official_account.models import OfficialAccount


class WechatTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def make_request(self):
        """
        生成一个虚拟的 Request 对象
        :return: request 实例
        """
        return RequestFactory().get('/')

    def make_verify_parameter(self, token):
        """
        生成微信请求的验证参数
        :param token: 微信 Token
        :return: (signature, timestamp, nonce)
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
        :return: 公众号实例 (OfficialAccount)
        """
        return OfficialAccount.manager.add(level, name, email, original, wechat, introduction, address,
                                           appid, appsecret, username, password, is_advanced, token)

    def make_msgid(self):
        """
        生成一个消息ID
        :return: 消息ID
        """
        return int(make_random_string(length=16, integer=True))

    def make_target(self):
        """
        生成一个目标OpenID
        :return: 目标OpenID
        """
        return make_random_string(length=29)

    def make_source(self):
        """
        生成一个来源OpenID
        :return: 来源OpenID
        """
        return make_random_string(length=29)

    def make_time(self):
        """
        生成当前时间的UNIX时间戳
        :return: 整型时间戳
        """
        return int(time.time())

    def make_url(self):
        """
        生成随机URL
        :return: URL地址
        """
        return 'http://test.oott.me/' + make_random_string(length=5)

    def make_raw_text_message(self, msgid=None, target=None, source=None, time=None, content=None):
        """
        生成文本消息请求的原生XML数据

        对应Keyword Argument如不提供，则自动随机
        :param msgid: 消息ID
        :param target: 目标用户OpenID
        :param source: 来源用户OpenID
        :param time: 信息发送时间
        :param content: 文本内容
        :return: XML
        """
        if not msgid:
            msgid = self.make_msgid()
        if not target:
            target = self.make_target()
        if not source:
            source = self.make_source()
        if not time:
            time = self.make_time()
        if not content:
            content = make_random_string(length=255)

        xml = u"""
        <xml>
        <ToUserName><![CDATA[{target}]]></ToUserName>
        <FromUserName><![CDATA[{source}]]></FromUserName>
        <CreateTime>{time}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{content}]]></Content>
        <MsgId>{msgid}</MsgId>
        </xml>
        """.format(
            target=target,
            source=source,
            time=time,
            content=content,
            msgid=msgid
        )

        return xml

    def make_raw_image_message(self, msgid=None, target=None, source=None, time=None, picurl=None):
        """
        生成图片消息请求的原生XML数据

        对应Keyword Argument如不提供，则自动随机
        :param msgid: 消息ID
        :param target: 目标用户OpenID
        :param source: 来源用户OpenID
        :param time: 信息发送时间
        :param picurl: 图片链接
        :return: XML
        """
        if not msgid:
            msgid = self.make_msgid()
        if not target:
            target = self.make_target()
        if not source:
            source = self.make_source()
        if not time:
            time = self.make_time()
        if not picurl:
            picurl = 'http://www.baidu.com/img/bd_logo1.png'

        xml = u"""
        <xml>
        <ToUserName><![CDATA[{target}]]></ToUserName>
        <FromUserName><![CDATA[{source}]]></FromUserName>
        <CreateTime>{time}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <PicUrl><![CDATA[{picurl}]]></PicUrl>
        <MediaId><![CDATA[media_id]]></MediaId>
        <MsgId>{msgid}</MsgId>
        </xml>
        """.format(
            target=target,
            source=source,
            time=time,
            picurl=picurl,
            msgid=msgid
        )

        return xml

    def make_raw_event_subscribe_message(self, target=None, source=None, time=None):
        """
        生成订阅事件消息请求的原生XML数据

        对应Keyword Argument如不提供，则自动随机
        :param target: 目标用户OpenID
        :param source: 来源用户OpenID
        :param time: 信息发送时间
        :return: XML
        """
        if not target:
            target = self.make_target()
        if not source:
            source = self.make_source()
        if not time:
            time = self.make_time()

        xml = u"""
        <xml>
        <ToUserName><![CDATA[{target}]]></ToUserName>
        <FromUserName><![CDATA[{source}]]></FromUserName>
        <CreateTime>{time}</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[subscribe]]></Event>
        </xml>
        """.format(
            target=target,
            source=source,
            time=time
        )

        return xml

    def make_raw_event_unsubscribe_message(self, target=None, source=None, time=None):
        """
        生成取消订阅事件消息请求的原生XML数据

        对应Keyword Argument如不提供，则自动随机
        :param target: 目标用户OpenID
        :param source: 来源用户OpenID
        :param time: 信息发送时间
        :return: XML
        """
        if not target:
            target = self.make_target()
        if not source:
            source = self.make_source()
        if not time:
            time = self.make_time()

        xml = u"""
        <xml>
        <ToUserName><![CDATA[{target}]]></ToUserName>
        <FromUserName><![CDATA[{source}]]></FromUserName>
        <CreateTime>{time}</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[unsubscribe]]></Event>
        </xml>
        """.format(
            target=target,
            source=source,
            time=time
        )

        return xml