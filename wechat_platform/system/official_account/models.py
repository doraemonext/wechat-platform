# -*- coding: utf-8 -*-

import logging

from django.db import models
from wechat_sdk import WechatBasic, WechatExt
from wechat_sdk.exceptions import OfficialAPIError, UnOfficialAPIError

from lib.tools.rand import make_unique_random_string
from system.official_account import OfficialAccountIncomplete, OfficialAccountIncorrect

logger_official_account = logging.getLogger(__name__)


class OfficialAccountManager(models.Manager):
    def add(self, level, name, email, original, wechat, introduction=None, address=None,
            appid=None, appsecret=None, username=None, password=None, is_advanced=False, token=None):
        """
        添加新公众号

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
        if not token:
            token = make_unique_random_string()

        official_account = super(OfficialAccountManager, self).create(
            iden=make_unique_random_string(),
            token=token,
            appid=appid,
            appsecret=appsecret,
            username=username,
            password=password,
            is_advanced=is_advanced,
            level=level,
            name=name,
            email=email,
            original=original,
            wechat=wechat,
            introduction=introduction,
            address=address
        )

        # 为默认回复插件添加规则及规则匹配
        rule = Rule.manager.add(
            official_account=official_account,
            name='_system_default_' + official_account.iden,
            reply_pattern=Rule.REPLY_PATTERN_RANDOM,
        )
        library_text = LibraryText.manager.add(
            official_account=official_account,
            content=u'此处为默认回复内容，请在后台更改',
        )
        rule_match = RuleMatch.manager.add(
            rule=rule,
            plugin_iden='text',
            reply_id=library_text.pk,
        )

        logger_official_account.debug('New model created with iden %s [Model] %s' % (official_account.iden, official_account.__dict__))
        return official_account


class OfficialAccount(models.Model):
    """
    公众号数据表
    """
    # 公众号级别
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    LEVEL = (
        (LEVEL_1, u'普通订阅号'),
        (LEVEL_2, u'认证订阅号/普通服务号'),
        (LEVEL_3, u'认证服务号'),
    )

    iden = models.CharField(u'公众号唯一标识', max_length=32)
    token = models.CharField(u'微信Token', max_length=300)
    appid = models.CharField(u'微信App ID', max_length=50, null=True, blank=True)
    appsecret = models.CharField(u'微信App Secret', max_length=50, null=True, blank=True)
    username = models.CharField(u'公众平台用户名', max_length=255, null=True, blank=True)
    password = models.CharField(u'公众平台密码', max_length=255, null=True, blank=True)
    is_advanced = models.BooleanField(u'是否开启高级支持', default=False)
    level = models.IntegerField(u'公众号级别', choices=LEVEL)
    name = models.CharField(u'公众号名称', max_length=100)
    email = models.EmailField(u'公众号登录邮箱', max_length=254)
    original = models.CharField(u'公众号原始ID', max_length=30)
    wechat = models.CharField(u'微信号', max_length=100)
    introduction = models.TextField(u'公众号介绍', null=True, blank=True)
    address = models.TextField(u'所在地址', null=True, blank=True)
    cache_access_token = models.CharField(u'缓存access token', max_length=512, blank=True, null=True)
    cache_access_token_expires_at = models.BigIntegerField(u'缓存access token过期时间', blank=True, null=True)
    cache_token = models.CharField(u'缓存模拟登陆token', max_length=512, blank=True, null=True)
    cache_cookies = models.TextField(u'缓存模拟登陆cookies', blank=True, null=True)

    manager = OfficialAccountManager()
    objects = models.Manager()

    class Meta:
        db_table = 'official_account'
        default_permissions = ('add', 'change', 'delete', 'view')

    def __unicode__(self):
        return self.name

    @property
    def simulation_available(self):
        """
        判断模拟登陆方式是否可用
        :return: 可用返回 True
        """
        return self.is_advanced and self.username and self.password

    @property
    def service_available(self):
        """
        判断多客服方式是否可用
        :return: 可用返回 True
        """
        return self.level == self.LEVEL_3 and self.appid and self.appsecret

    @property
    def has_token_cookies(self):
        """
        判断当前是否已经缓存 token 和 cookies
        :return: 已经缓存则返回 True
        """
        return self.cache_token and self.cache_cookies

    def get_cache_access_token(self, force_update=False):
        """
        获取缓存的access_token
        :param force_update: 强制刷新access_token
        :return: dict, exp: {'access_token': 'access_token', 'access_token_expires_at': 1234241244}
        :raise OfficialAccountIncomplete: 当公众号中不存在appid或appsecret时抛出
        :raise OfficialAccountIncorrect: 当公众号appid或apppsecret非法时抛出
        """
        if not self.appid or not self.appsecret:
            logger_official_account.warning('Lack of appid or appsecret in the official account [Model] %s' % self.__dict__)
            raise OfficialAccountIncomplete('Lack of appid or appsecret in the official account')

        if force_update:
            wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret)
        else:
            wechat = WechatBasic(appid=self.appid, appsecret=self.appsecret, access_token=self.cache_access_token,
                                 access_token_expires_at=self.cache_access_token_expires_at)
        try:
            access_token_dict = wechat.get_access_token()
        except OfficialAPIError, e:
            logger_official_account.error('AppID or AppSecret is incorrect [Detail] %s [Model] %s' % (e, self.__dict__))
            raise OfficialAccountIncorrect('AppID or AppSecret is incorrect')

        # 更新自身的access_token及access_token_expires_at
        if self.cache_access_token != access_token_dict['access_token'] or self.cache_access_token_expires_at != access_token_dict['access_token_expires_at']:
            logger_official_account.debug('Ready to update the model [Model] %s' % self.__dict__)
            self.cache_access_token = access_token_dict['access_token']
            self.cache_access_token_expires_at = access_token_dict['access_token_expires_at']
            self.save()
            logger_official_account.debug('The model has been updated [Model] %s' % self.__dict__)

        return access_token_dict

    def set_cache_access_token(self, access_token_dict=None, access_token=None, access_token_expires_at=None):
        """
        设置缓存access_token

        access_token_dict 和 access_token/access_token_expires_at 任选一组提供
        :param access_token_dict: Access Token 组合字典 (WechatBasic的get_access_token()返回值), exp:
                                  {'access_token': 'access_token', 'access_token_expires_at': 1234241244}
        :param access_token: Access Token
        :param access_token_expires_at: Access Token 过期日期
        """
        logger_official_account.debug('Ready to update the model [Model] %s' % self.__dict__)
        if access_token_dict:
            self.cache_access_token = access_token_dict['access_token']
            self.cache_access_token_expires_at = access_token_dict['access_token_expires_at']
        elif access_token and access_token_expires_at:
            self.cache_access_token = access_token
            self.cache_access_token_expires_at = access_token_expires_at
        else:
            raise AttributeError('must provide one of the keyword argument groups')
        self.save()
        logger_official_account.debug('The model has been updated [Model] %s' % self.__dict__)

    def get_cache_token_cookies(self):
        """
        获取缓存的模拟登陆token和cookies
        :return: dict, exp: {'token': 'token', 'cookies': 'cookies string'}
        """
        return {
            'token': self.cache_token,
            'cookies': self.cache_cookies,
        }

    def set_cache_token_cookies(self, token_cookies_dict=None, token=None, cookies=None):
        """
        设置缓存token及cookies

        token_cookies_dict 和 token/cookies 任选一组提供
        :param token_cookies_dict: Token及Cookies 组合字典 (WechatExt的get_token_cookies()返回值), exp:
                                   {'token': 'token', 'cookies': 'cookies string'}
        :param token: Token
        :param cookies: Cookie
        """
        logger_official_account.debug('Ready to update the model [Model] %s' % self.__dict__)
        if token_cookies_dict:
            self.cache_token = token_cookies_dict['token']
            self.cache_cookies = token_cookies_dict['cookies']
        elif token and cookies:
            self.cache_token = token
            self.cache_cookies = cookies
        else:
            raise AttributeError('must provide one of the keyword argument groups')
        self.save()
        logger_official_account.debug('The model has been updated [Model] %s' % self.__dict__)


from system.rule.models import Rule
from system.rule_match.models import RuleMatch
from system.library.text.models import LibraryText