# -*- coding: utf-8 -*-

from django.db import models

from lib.tools.random import make_random_string


class OfficialAccountManager(models.Manager):
    def add(self, level, name, email, original, wechat, introduction=None, address=None,
            appid=None, appsecret=None, username=None, password=None, token=None):
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
        :param token: 微信 Token, 如不传入将自动生成
        """
        if not token:
            token = make_random_string()

        return super(OfficialAccountManager, self).create(
            iden=make_random_string(),
            token=token,
            appid=appid,
            appsecret=appsecret,
            username=username,
            password=password,
            level=level,
            name=name,
            email=email,
            original=original,
            wechat=wechat,
            introduction=introduction,
            address=address
        )


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
    level = models.IntegerField(u'公众号级别', choices=LEVEL)
    name = models.CharField(u'公众号名称', max_length=100)
    email = models.EmailField(u'公众号登录邮箱', max_length=254)
    original = models.CharField(u'公众号原始ID', max_length=30)
    wechat = models.CharField(u'微信号', max_length=100)
    introduction = models.TextField(u'公众号介绍', null=True, blank=True)
    address = models.TextField(u'所在地址', null=True, blank=True)

    manager = OfficialAccountManager()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'official_account'