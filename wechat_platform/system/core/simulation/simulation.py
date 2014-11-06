# -*- coding: utf-8 -*-

import logging
import json
import tempfile
from collections import OrderedDict

from wechat_sdk import WechatExt
from wechat_sdk.exceptions import UnOfficialAPIError, NeedLoginError, LoginError, LoginVerifyCodeError

from system.core.simulation import SimulationException
from system.core.captcha import Captcha
from system.core.captcha import CaptchaException

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
            return
        except LoginVerifyCodeError, e:
            for x in range(0, 3):  # 对于验证码重试3次
                fd, name = tempfile.mkstemp()
                self.wechat_ext.get_verify_code(file_path=name)
                try:
                    self.wechat_ext.login(verify_code=Captcha(file_path=name).recognition())
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
                if item.get('date_time') == self.message.time and item.get('type') == self.TYPE_TEXT and item.get('content') == self.message.content:
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
        :return:
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

    def send_message(self, fakeid, content):
        """
        主动发送文本消息
        :param fakeid: 用户的 UID (即 fakeid )
        :param content: 发送的内容
        :raises ValueError: 参数出错, 具体内容有 ``fake id not exist``
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