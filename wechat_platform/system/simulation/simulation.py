# -*- coding: utf-8 -*-

import logging
import json
import tempfile
from collections import OrderedDict

from wechat_sdk import WechatExt
from wechat_sdk.exceptions import NeedLoginError, LoginError, LoginVerifyCodeError

from system.simulation import SimulationException
from system.core.captcha import Captcha, CaptchaException


logger_simulation = logging.getLogger(__name__)


class Simulation(object):
    """
    模拟登陆辅助类
    """
    TYPE_TEXT = 1  # 文本类型
    TYPE_LOCATION = 1  # 地理位置类型
    TYPE_IMAGE = 2  # 图片类型
    TYPE_VOICE = 3  # 语音类型
    TYPE_VIDEO = 4  # 视频类型
    TYPE_LINK = 5  # 链接类型

    def __init__(self, official_account, wechat_basic, wechat_ext=None, username=None, password=None):
        """
        模拟登陆辅助类初始化

        wechat_ext 和 username/password 任提供一组即可, 提供 wechat_ext 参数则默认其已经初始化完毕, 提供 username 和 password
        则由本类执行初始化操作
        :param official_account: 公众号实例 (OfficialAccount)
        :param wechat_basic: 微信官方操作实例 (WechatBasic)
        :param wechat_ext: 微信非官方操作实例 (WechatExt)
        :param username: 微信公众平台登录用户名
        :param password: 微信公众平台登录密码
        """
        self.official_account = official_account
        self.wechat_basic = wechat_basic
        self.message = self.wechat_basic.get_message()
        if wechat_ext:
            self.wechat_ext = wechat_ext
        elif username and password:
            self.wechat_ext = WechatExt(username=username, password=password, login=False)
            try:
                self.login()
            except LoginError, e:
                logger_simulation.error('Simulated login failed: %s [OfficialAccount] %s [WechatBasic] %s [WechatExt] username: \'%s\' password: \'%s\'' % (
                    e,
                    self.official_account.__dict__,
                    self.wechat_basic.__dict__,
                    username,
                    password,
                ))
                raise SimulationException(e)
        else:
            raise SimulationException('the initialization parameter is insufficient')

    def login(self):
        """
        登录微信公众平台

        如果不需要验证码则直接登录, 需要验证码将会自动识别(需在后台配置人工识别验证码接口), 在识别结果不正确情况下会重试3次
        :raise LoginError: 当无法登录时抛出
        """
        try:
            self.wechat_ext.login()
            self.official_account.set_cache_token_cookies(self.wechat_ext.get_token_cookies())
            self.official_account.save()
            logger_simulation.debug('Successful simulated login without captcha')
            return
        except LoginVerifyCodeError:
            for x in range(0, 3):  # 对于验证码重试3次
                fd, name = tempfile.mkstemp()
                self.wechat_ext.get_verify_code(file_path=name)
                try:
                    self.wechat_ext.login(verify_code=Captcha(file_path=name).recognition())
                    self.official_account.set_cache_token_cookies(self.wechat_ext.get_token_cookies())
                    self.official_account.save()
                    logger_simulation.debug('Successful simulated login with captcha')
                    return
                except (CaptchaException, LoginVerifyCodeError):
                    pass  # 此处直接忽略, 进行下一次重试

    def find_latest_user(self, count=20):
        """
        从公众平台抓取最新的消息列表和当前的 wechat 请求匹配, 找出该请求所对应的人在公众平台中的唯一标识符 fakeid

        注意: 如果并发量过大导致获取的 fakeid 列表为空, 请适当调高 count 参数值, 理想情况下返回的 fakeid 列表只会存在一个用户,
        如果列表中存在不只一个用户的 fakeid, 说明匹配到多个用户, 无法精确匹配, 请妥善处理
        :param count: 抓取消息列表中的消息个数, 推荐为 20 , 无特殊需要不需修改
        :return: 返回一个列表, 列表中的每个元素为匹配到的用户 fakeid , 理想情况下列表中只会有一个 fakeid 存在
        """
        message_list = self.get_message_list(count=count)
        fakeid_list = []
        for item in message_list['msg_item']:
            if self.message.type == 'text':
                if abs(item.get('date_time') - self.message.time) <= 1 and item.get('type') == self.TYPE_TEXT and item.get('content') == self.message.content:
                    fakeid_list.append(item.get('fakeid'))
            elif self.message.type == 'location':
                if item.get('date_time') == self.message.time and item.get('type') == self.TYPE_LOCATION:
                    fakeid_list.append(item.get('fakeid'))
            elif self.message.type == 'image':
                if item.get('date_time') == self.message.time and item.get('type') == self.TYPE_IMAGE:
                    fakeid_list.append(item.get('fakeid'))
            elif self.message.type == 'voice':
                if item.get('date_time') == self.message.time and item.get('type') == self.TYPE_VOICE:
                    fakeid_list.append(item.get('fakeid'))
            elif self.message.type == 'video':
                if item.get('date_time') == self.message.time and item.get('type') == self.TYPE_VIDEO:
                    fakeid_list.append(item.get('fakeid'))
            elif self.message.type == 'link':
                if item.get('date_time') == self.message.time and item.get('type') == self.TYPE_LINK:
                    fakeid_list.append(item['fakeid'])

        return list(OrderedDict.fromkeys(fakeid_list))

    def get_message_list(self, lastid=0, offset=0, count=20, day=7, star=False):
        """
        获取消息列表
        :param lastid: 传入最后的消息 id 编号, 为 0 则从最新一条起倒序获取
        :param offset: lastid 起算第一条的偏移量
        :param count: 获取数目
        :param day: 最近几天消息 (0: 今天, 1: 昨天, 2: 前天, 3: 更早, 7: 全部), 这里的全部仅有5天
        :param star: 是否只获取星标消息
        :return: 返回的数据, dict形式
        :raises SimulationException: 当模拟登陆登录失败时抛出
        """
        for i in range(0, 2):
            try:
                try:
                    message_list_json = self.wechat_ext.get_message_list(lastid=lastid, offset=offset, count=count, day=day, star=star)
                    return json.loads(message_list_json)
                except NeedLoginError, e:
                    self.login()
            except LoginError, e:
                logger_simulation.error('Simulated login failed: %s [OfficialAccount] %s [WechatBasic] %s [WechatExt] %s' % (
                    e,
                    self.official_account.__dict__,
                    self.wechat_basic.__dict__,
                    self.wechat_ext.__dict__,
                ))
                raise SimulationException(e)
        logger_simulation.error('Simulated login failed [OfficialAccount] %s [WechatBasic] %s [WechatExt] %s' % (
            self.official_account.__dict__,
            self.wechat_basic.__dict__,
            self.wechat_ext.__dict__,
        ))
        raise SimulationException('login error')

    def get_news_list(self, page, pagesize=10):
        """
        获取图文信息列表

        返回JSON示例::

            [
                {
                    "multi_item": [
                        {
                            "seq": 0,
                            "title": "98路公交线路",
                            "show_cover_pic": 1,
                            "author": "",
                            "cover": "https://mmbiz.qlogo.cn/mmbiz/D2pflbZwStFibz2Sb1kWOuHrxtDMPKJic3GQgcgkDSoEm668gClFVDt3BR8GGQ5eB8HoL4vDezzKtSblIjckOf7A/0",
                            "content_url": "http://mp.weixin.qq.com/s?__biz=MjM5MTA2ODcwOA==&mid=204884970&idx=1&sn=bf25c51f07260d4ed38305a1cbc0ce0f#rd",
                            "source_url": "",
                            "file_id": 204884939,
                            "digest": "98路线路1.农大- 2.金阳小区- 3.市客运司- 4.市制药厂- 5.新农大- 6.独山子酒店- 7.三"
                        }
                    ],
                    "seq": 0,
                    "title": "98路公交线路",
                    "show_cover_pic": 1,
                    "author": "",
                    "app_id": 204884970,
                    "content_url": "http://mp.weixin.qq.com/s?__biz=MjM5MTA2ODcwOA==&mid=204884970&idx=1&sn=bf25c51f07260d4ed38305a1cbc0ce0f#rd",
                    "create_time": "1405237966",
                    "file_id": 204884939,
                    "img_url": "https://mmbiz.qlogo.cn/mmbiz/D2pflbZwStFibz2Sb1kWOuHrxtDMPKJic3GQgcgkDSoEm668gClFVDt3BR8GGQ5eB8HoL4vDezzKtSblIjckOf7A/0",
                    "digest": "98路线路1.农大- 2.金阳小区- 3.市客运司- 4.市制药厂- 5.新农大- 6.独山子酒店- 7.三"
                },
                {
                    "multi_item": [
                        {
                            "seq": 0,
                            "title": "2013年新疆软件园大事记",
                            "show_cover_pic": 0,
                            "author": "",
                            "cover": "https://mmbiz.qlogo.cn/mmbiz/D2pflbZwStFibz2Sb1kWOuHrxtDMPKJic3icvFgkxZRyIrkLbic9I5ZKLa3XB8UqNlkT8CYibByHuraSvVoeSzdTRLQ/0",
                            "content_url": "http://mp.weixin.qq.com/s?__biz=MjM5MTA2ODcwOA==&mid=204883415&idx=1&sn=68d62215052d29ece3f2664e9c4e8cab#rd",
                            "source_url": "",
                            "file_id": 204883412,
                            "digest": "1月1．新疆软件园展厅设计方案汇报会2013年1月15日在维泰大厦4楼9号会议室召开新疆软件园展厅设计工作完"
                        },
                        {
                            "seq": 1,
                            "title": "2012年新疆软件园大事记",
                            "show_cover_pic": 0,
                            "author": "",
                            "cover": "https://mmbiz.qlogo.cn/mmbiz/D2pflbZwStFibz2Sb1kWOuHrxtDMPKJic3oErGEhSicRQc82icibxZOZ2YAGNgiaGYfOFYppmPzOOS0v1xfZ1nvyT58g/0",
                            "content_url": "http://mp.weixin.qq.com/s?__biz=MjM5MTA2ODcwOA==&mid=204883415&idx=2&sn=e7db9b30d770c85c61008d2f523b8610#rd",
                            "source_url": "",
                            "file_id": 204883398,
                            "digest": "1月1．新疆软件园环评顺利通过专家会评审2012年1月30日，新疆软件园环境影响评价顺利通过专家会评审，与会"
                        },
                        {
                            "seq": 2,
                            "title": "2011年新疆软件园大事记",
                            "show_cover_pic": 0,
                            "author": "",
                            "cover": "https://mmbiz.qlogo.cn/mmbiz/D2pflbZwStFibz2Sb1kWOuHrxtDMPKJic3qA7tEN8GvkgDwnOfKsGsicJeQ6PxQSgWuJXfQaXkpM4VNlQicOWJM4Tg/0",
                            "content_url": "http://mp.weixin.qq.com/s?__biz=MjM5MTA2ODcwOA==&mid=204883415&idx=3&sn=4cb1c6d25cbe6dfeff37f52a62532bd0#rd",
                            "source_url": "",
                            "file_id": 204883393,
                            "digest": "6月1．软件园召开第一次建设领导小组会议2011年6月7日，第一次软件园建设领导小组会议召开，会议认为，新疆"
                        },
                        {
                            "seq": 3,
                            "title": "2010年新疆软件园大事记",
                            "show_cover_pic": 0,
                            "author": "",
                            "cover": "https://mmbiz.qlogo.cn/mmbiz/D2pflbZwStFibz2Sb1kWOuHrxtDMPKJic3YG4sSuf9X9ecMPjDRju842IbIvpFWK7tuZs0Po4kZCz4URzOBj5rnQ/0",
                            "content_url": "http://mp.weixin.qq.com/s?__biz=MjM5MTA2ODcwOA==&mid=204883415&idx=4&sn=4319f7f051f36ed972e2f05a221738ec#rd",
                            "source_url": "",
                            "file_id": 204884043,
                            "digest": "5月1．新疆软件园与开发区（头屯河区）管委会、经信委签署《新疆软件园建设战略合作协议》2010年5月12日，"
                        }
                    ],
                    "seq": 1,
                    "title": "2013年新疆软件园大事记",
                    "show_cover_pic": 0,
                    "author": "",
                    "app_id": 204883415,
                    "content_url": "http://mp.weixin.qq.com/s?__biz=MjM5MTA2ODcwOA==&mid=204883415&idx=1&sn=68d62215052d29ece3f2664e9c4e8cab#rd",
                    "create_time": "1405232974",
                    "file_id": 204883412,
                    "img_url": "https://mmbiz.qlogo.cn/mmbiz/D2pflbZwStFibz2Sb1kWOuHrxtDMPKJic3icvFgkxZRyIrkLbic9I5ZKLa3XB8UqNlkT8CYibByHuraSvVoeSzdTRLQ/0",
                    "digest": "1月1．新疆软件园展厅设计方案汇报会2013年1月15日在维泰大厦4楼9号会议室召开新疆软件园展厅设计工作完"
                }
            ]

        :param page: 页码 (从 0 开始)
        :param pagesize: 每页数目
        :return: 返回的数据, dict形式
        :raises SimulationException: 当模拟登陆登录失败时抛出
        """
        for i in range(0, 2):
            try:
                try:
                    news_list_json = self.wechat_ext.get_news_list(page=page, pagesize=pagesize)
                    return json.loads(news_list_json)
                except NeedLoginError, e:
                    self.login()
            except LoginError, e:
                logger_simulation.error('Simulated login failed: %s [OfficialAccount] %s [WechatBasic] %s [WechatExt] %s' % (
                    e,
                    self.official_account.__dict__,
                    self.wechat_basic.__dict__,
                    self.wechat_ext.__dict__,
                ))
                raise SimulationException(e)
        logger_simulation.error('Simulated login failed [OfficialAccount] %s [WechatBasic] %s [WechatExt] %s' % (
            self.official_account.__dict__,
            self.wechat_basic.__dict__,
            self.wechat_ext.__dict__,
        ))
        raise SimulationException('login error')

    def send_message(self, fakeid, content):
        """
        主动发送文本消息
        :param fakeid: 用户的 UID (即 fakeid )
        :param content: 发送的内容
        :raises ValueError: 参数出错, 具体内容有 ``fake id not exist``
        :raises SimulationException: 当模拟登陆登录失败时抛出
        """
        for i in range(0, 2):
            try:
                try:
                    self.wechat_ext.send_message(fakeid=fakeid, content=content)
                    return
                except NeedLoginError:
                    self.login()
            except LoginError, e:
                logger_simulation.error('Simulated login failed: %s [OfficialAccount] %s [WechatBasic] %s [WechatExt] %s' % (
                    e,
                    self.official_account.__dict__,
                    self.wechat_basic.__dict__,
                    self.wechat_ext.__dict__,
                ))
                raise SimulationException(e)
        logger_simulation.error('Simulated login failed [OfficialAccount] %s [WechatBasic] %s [WechatExt] %s' % (
            self.official_account.__dict__,
            self.wechat_basic.__dict__,
            self.wechat_ext.__dict__,
        ))
        raise SimulationException('login error')

    def send_news(self, fakeid, msgid):
        """
        主动发送图文信息
        :param fakeid: 用户的 UID (即 fakeid )
        :param msgid: 图文
        :raises ValueError: 参数出错, 具体内容有 'fake id not exist' 及 'message id not exist'
        :raises SimulationException: 当模拟登陆登录失败时抛出
        """
        for i in range(0, 2):
            try:
                try:
                    self.wechat_ext.send_news(fakeid=fakeid, msgid=msgid)
                    return
                except NeedLoginError:
                    self.login()
            except LoginError, e:
                logger_simulation.error('Simulated login failed: %s [OfficialAccount] %s [WechatBasic] %s [WechatExt] %s' % (
                    e,
                    self.official_account.__dict__,
                    self.wechat_basic.__dict__,
                    self.wechat_ext.__dict__,
                ))
                raise SimulationException(e)
        logger_simulation.error('Simulated login failed [OfficialAccount] %s [WechatBasic] %s [WechatExt] %s' % (
            self.official_account.__dict__,
            self.wechat_basic.__dict__,
            self.wechat_ext.__dict__,
        ))
        raise SimulationException('login error')

    def add_news(self, news):
        """
        在素材库中创建图文消息

        :param news: list 对象, 其中的每个元素为一个 dict 对象, 代表一条图文, key 值分别为 ``title``, ``author``, ``summary``,
                     ``content``, ``picid``, ``from_url``, 对应内容为标题, 作者, 摘要, 内容, 素材库里的
                     图片ID(可通过 ``upload_file`` 函数上传获取), 来源链接。

                     其中必须提供的 key 值为 ``title`` 和 ``content``

                     示例::

                         [
                             {
                                 'title': '图文标题',
                                 'author': '图文作者',
                                 'summary': '图文摘要',
                                 'content': '图文内容',
                                 'picid': '23412341',
                                 'from_url': 'http://www.baidu.com',
                             },
                             {
                                 'title': '最少图文标题',
                                 'content': '图文内容',
                             }
                         ]
        :raises ValueError: 参数提供错误时抛出
        :raises SimulationException: 当模拟登陆登录失败时抛出
        """
        for i in range(0, 2):
            try:
                try:
                    self.wechat_ext.add_news(news=news)
                    return
                except NeedLoginError:
                    self.login()
            except LoginError, e:
                logger_simulation.error('Simulated login failed: %s [OfficialAccount] %s [WechatBasic] %s [WechatExt] %s' % (
                    e,
                    self.official_account.__dict__,
                    self.wechat_basic.__dict__,
                    self.wechat_ext.__dict__,
                ))
                raise SimulationException(e)
        logger_simulation.error('Simulated login failed [OfficialAccount] %s [WechatBasic] %s [WechatExt] %s' % (
            self.official_account.__dict__,
            self.wechat_basic.__dict__,
            self.wechat_ext.__dict__,
        ))
        raise SimulationException('login error')

    def upload_file(self, filepath):
        """
        上传素材 (图片/音频/视频)
        :param filepath: 本地文件路径
        :return: 直接返回上传后的文件 ID (fid)
        :raises ValueError: 参数出错, 错误原因直接打印异常即可 (常见错误内容: ``file not exist``: 找不到本地文件, ``audio too long``: 音频文件过长, ``file invalid type``: 文件格式不正确, 还有其他错误请自行检查)
        :raises SimulationException: 当模拟登陆登录失败时抛出
        """
        for i in range(0, 2):
            try:
                try:
                    return self.wechat_ext.upload_file(filepath=str(filepath))
                except NeedLoginError:
                    self.login()
            except LoginError, e:
                logger_simulation.error('Simulated login failed: %s [OfficialAccount] %s [WechatBasic] %s [WechatExt] %s' % (
                    e,
                    self.official_account.__dict__,
                    self.wechat_basic.__dict__,
                    self.wechat_ext.__dict__,
                ))
                raise SimulationException(e)
        logger_simulation.error('Simulated login failed [OfficialAccount] %s [WechatBasic] %s [WechatExt] %s' % (
            self.official_account.__dict__,
            self.wechat_basic.__dict__,
            self.wechat_ext.__dict__,
        ))
        raise SimulationException('login error')

    def send_file(self, fakeid, fid, type):
        """
        向特定用户发送媒体文件
        :param fakeid: 用户 UID (即 fakeid)
        :param fid: 文件 ID
        :param type: 文件类型 (2: 图片, 3: 音频)
        :raises ValueError: 参数出错, 错误原因直接打印异常即可 (常见错误内容: ``system error`` 或 ``can not send this type of msg``: 文件类型不匹配, ``user not exist``: 用户 fakeid 不存在, ``file not exist``: 文件 fid 不存在, 还有其他错误请自行检查)
        :raises SimulationException: 当模拟登陆登录失败时抛出
        """
        for i in range(0, 2):
            try:
                try:
                    return self.wechat_ext.send_file(fakeid=fakeid, fid=fid, type=type)
                except NeedLoginError:
                    self.login()
            except LoginError, e:
                logger_simulation.error('Simulated login failed: %s [OfficialAccount] %s [WechatBasic] %s [WechatExt] %s' % (
                    e,
                    self.official_account.__dict__,
                    self.wechat_basic.__dict__,
                    self.wechat_ext.__dict__,
                ))
                raise SimulationException(e)
        logger_simulation.error('Simulated login failed [OfficialAccount] %s [WechatBasic] %s [WechatExt] %s' % (
            self.official_account.__dict__,
            self.wechat_basic.__dict__,
            self.wechat_ext.__dict__,
        ))
        raise SimulationException('login error')

    def send_image(self, fakeid, fid):
        """
        给指定用户 fakeid 发送图片信息
        :param fakeid: 用户的 UID (即 fakeid)
        :param fid: 文件 ID
        :raises ValueError: 参数出错, 错误原因直接打印异常即可 (常见错误内容: ``system error`` 或 ``can not send this type of msg``: 文件类型不匹配, ``user not exist``: 用户 fakeid 不存在, ``file not exist``: 文件 fid 不存在, 还有其他错误请自行检查)
        :raises SimulationException: 当模拟登陆登录失败时抛出
        """
        return self.send_file(fakeid, fid, 2)

    def send_audio(self, fakeid, fid):
        """
        给指定用户 fakeid 发送语音信息
        :param fakeid: 用户的 UID (即 fakeid)
        :param fid: 文件 ID
        :raises ValueError: 参数出错, 错误原因直接打印异常即可 (常见错误内容: ``system error`` 或 ``can not send this type of msg``: 文件类型不匹配, ``user not exist``: 用户 fakeid 不存在, ``file not exist``: 文件 fid 不存在, 还有其他错误请自行检查)
        :raises SimulationException: 当模拟登陆登录失败时抛出
        """
        return self.send_file(fakeid, fid, 3)
