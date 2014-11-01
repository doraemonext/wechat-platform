# -*- coding: utf-8 -*-

import os
import sys
from imp import find_module, load_module, acquire_lock, release_lock

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from wechat_sdk import WechatExt

from system.core.exceptions import PluginLoadError, PluginResponseError
from system.official_account.models import OfficialAccount
from .models import Plugin


class PluginProcessor(object):
    """
    插件响应过程基类, 每个插件响应过程都要在此基础上进行扩展
    """
    def __init__(self, official_account, wechat, context, message=None, in_context=False, is_exclusive=False, plugin=None, is_system=False, **kwargs):
        """
        初始化插件, 将状态信息存储
        :param official_account: 公众号实例 (OfficialAccount)
        :param wechat: 微信请求实例 (WechatBasic)
        :param context: 微信上下文对话实例 (DatabaseContextStore)
        :param message: 微信请求信息实例 (WechatMessage)
        :param in_context: 当前是否在上下文对话过程中
        :param is_exclusive: 插件是否可以独享响应内容
        :param plugin: 插件信息实例 (Plugin)
        :param is_system: 是否为系统插件
        """
        self.official_account = official_account
        self.wechat = wechat
        self.context = context
        if not message:
            self.message = self.wechat.get_message()
        else:
            self.message = message
        self.in_context = in_context
        self.is_exclusive = is_exclusive
        self.plugin = plugin
        self.is_system = is_system

    def begin_context(self):
        """
        开始上下文对话模式
        """
        self.context['_plugin_iden'] = self.plugin.iden
        self.in_context = True

    def end_context(self):
        """
        结束上下文对话
        """
        try:
            del self.context['_plugin_iden']
        except KeyError:
            pass
        self.in_context = False

    def response_text(self, text, pattern='auto'):
        """
        向用户发送文字信息
        :param text: 文本内容
        :param pattern: 发送模式, 可选字符串: 'auto'(自动选择), 'basic'(基本被动响应发送模式), 'service'(多客服发送模式),
                        'simulation'(模拟登陆发送模式)
        """
        if pattern == 'auto':
            pattern = self._best_pattern(response_type='text')

        if pattern == 'basic':
            return self.wechat.response_text(content=text)
        elif pattern == 'service':
            raise Exception('have not yet implemented')
        else:
            token_cookies_dict = self.official_account.get_cache_token_cookies()
            wechat = WechatExt(username=self.official_account.username, password=self.official_account.password,
                               token=token_cookies_dict['token'], cookies=token_cookies_dict['cookies'])

            raise Exception('have not yet implemented')

    def response_image(self, mid):
        pass

    def response_voice(self, mid):
        pass

    def response_video(self, video):
        pass

    def response_music(self, music):
        pass

    def response_news(self, news):
        pass

    def response(self):
        """
        响应函数, 由继承的类进行扩展, 当对本插件初始化完成后, 调用此函数即可得到响应结果
        """
        raise NotImplementedError('subclasses of PluginProcess must provide an response() method')

    def _best_pattern(self, response_type):
        """
        根据返回类型选择最恰当的返回方法
        :param response_type: 返回信息类型
        :return: 返回方法字符串
        """
        if self.official_account.level in [OfficialAccount.LEVEL_1, OfficialAccount.LEVEL_2]:
            if response_type in ['text', 'music', 'news'] and self.is_exclusive:
                return 'basic'
            elif self.official_account.is_advanced and self.official_account.username and self.official_account.password:
                return 'simulation'
            else:
                raise PluginResponseError('no method available to response message')
        else:
            if response_type in ['text', 'music', 'news', 'image', 'voice', 'video'] and self.is_exclusive:
                return 'basic'
            else:
                return 'service'


class PluginProcessorSystem(PluginProcessor):
    """
    系统插件响应过程基类, 每个系统插件响应过程都要在此基础上进行扩展
    """
    def __init__(self, *args, **kwargs):
        super(PluginProcessorSystem, self).__init__(*args, **kwargs)
        self.reply_id = kwargs.get('reply_id')


def load_plugin(official_account, wechat, context, message=None, in_context=False, is_exclusive=False, plugin=None, is_system=False, **kwargs):
    """
    加载插件并做初始化工作，返回插件实例 (PluginProcess)
    :param official_account: 公众号实例 (OfficialAccount)
    :param wechat: 微信请求实例 (WechatBasic)
    :param context: 微信上下文对话实例 (DatabaseContextStore)
    :param message: 微信请求信息实例 (WechatMessage)
    :param in_context: 当前是否在上下文对话过程中
    :param is_exclusive: 插件是否可以独享响应内容
    :param plugin: 插件信息实例 (Plugin)
    :param is_system: 是否为系统插件

    :param reply_id: (hidden) 系统插件可选传入, 作为库ID使用
    """
    if is_system:
        directory = os.path.join(settings.PROJECT_DIR, 'plugins/system')
    else:
        directory = os.path.join(settings.PROJECT_DIR, 'plugins')

    try:
        full_path = os.path.join(directory, plugin.iden)
        if not os.path.isdir(full_path):
            raise PluginLoadError('plugin folder does not exist')
        if not os.path.exists(os.path.join(full_path, 'process.py')):
            raise PluginLoadError('the process.py file does not exist in the plugins folder')
    except OSError:
        raise PluginLoadError('error when accessing plugin folder')

    fh = None
    mod = None
    try:
        acquire_lock()
        fh, filename, desc = find_module("process", [os.path.join(directory, plugin.iden)])
        old = sys.modules.get(plugin.iden)
        if old is not None:
            del sys.modules[plugin.iden]
        mod = load_module(plugin.iden, fh, filename, desc)
    finally:
        if fh:
            fh.close()
        release_lock()
    if hasattr(mod, "__all__"):
        attrs = [getattr(mod, x) for x in mod.__all__]
        for plug in attrs:
            if is_system:
                if issubclass(plug, PluginProcessorSystem):
                    return plug(
                        official_account=official_account,
                        wechat=wechat,
                        context=context,
                        message=message,
                        in_context=in_context,
                        is_exclusive=is_exclusive,
                        plugin=plugin,
                        is_system=is_system,
                        reply_id=kwargs.get('reply_id')
                    )
            else:
                if issubclass(plug, PluginProcessor):
                    return plug(
                        official_account=official_account,
                        wechat=wechat,
                        context=context,
                        message=message,
                        in_context=in_context,
                        is_exclusive=is_exclusive,
                        plugin=plugin,
                        is_system=is_system
                    )
    raise PluginLoadError('you should set __all__ variable in process.py')