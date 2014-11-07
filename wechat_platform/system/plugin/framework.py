# -*- coding: utf-8 -*-

import logging
import os
import sys
from imp import find_module, load_module, acquire_lock, release_lock

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from wechat_sdk import WechatExt

from system.core.simulation import Simulation
from system.official_account.models import OfficialAccount
from system.plugin import PluginLoadError, PluginResponseError
from system.plugin.models import Plugin
from system.response.models import Response

logger_plugin = logging.getLogger(__name__)


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
            if not self.official_account.simulation_available:
                logger_plugin.debug('Simulation is not available in current settings [OfficialAccount] %s' % self.official_account.__dict__)
                raise PluginResponseError('Simulation is not available in current settings')

            if self.official_account.has_token_cookies:  # 当已经存在缓存的 token 和 cookies 时直接利用它们初始化
                token_cookies_dict = self.official_account.get_cache_token_cookies()
                wechat_ext = WechatExt(
                    username=self.official_account.username,
                    password=self.official_account.password,
                    token=token_cookies_dict['token'],
                    cookies=token_cookies_dict['cookies'],
                )
                simulation = Simulation(
                    official_account=self.official_account,
                    wechat_basic=self.wechat,
                    wechat_ext=wechat_ext
                )
            else:  # 当不存在缓存的 token 和 cookies 时利用用户名密码初始化
                simulation = Simulation(
                    official_account=self.official_account,
                    wechat_basic=self.wechat,
                    username=self.official_account.username,
                    password=self.official_account.password,
                )

            fakeid_list = simulation.find_latest_user()
            if len(fakeid_list) == 1:
                logger_plugin.debug('A user matched [FakeidList] %s [OfficialAccount] %s' % (fakeid_list, self.official_account.__dict__))
                simulation.send_message(fakeid=fakeid_list[0], content=text)
                Response.manager.add(
                    official_account=self.official_account,
                    wechat_instance=self.wechat,
                    type=Response.TYPE_TEXT,
                    pattern=Response.PATTERN_SIMULATION,
                    raw=text,
                    plugin_dict={
                        'iden': 'text',
                        'reply_id': self.reply_id,
                    }
                )
                return None
            elif len(fakeid_list) == 0:
                logger_plugin.debug('No user matched [OfficialAccount] %s' % self.official_account.__dict__)
                raise PluginResponseError('No user matched')
            else:
                logger_plugin.debug('Multiple users matched [FakeidList] %s [OfficialAccount] %s' % (fakeid_list, self.official_account.__dict__))
                raise PluginResponseError('Multiple users matched')

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


def load_plugin(official_account, wechat, context, plugin,  message=None, in_context=False, is_exclusive=False, is_system=False, **kwargs):
    """
    加载插件并做初始化工作，返回插件实例 (PluginProcess)
    :param official_account: 公众号实例 (OfficialAccount)
    :param wechat: 微信请求实例 (WechatBasic)
    :param context: 微信上下文对话实例 (DatabaseContextStore)
    :param plugin: 插件信息实例 (Plugin)
    :param message: 微信请求信息实例 (WechatMessage)
    :param in_context: 当前是否在上下文对话过程中
    :param is_exclusive: 插件是否可以独享响应内容
    :param is_system: 是否为系统插件

    :param reply_id: (hidden) 系统插件可选传入, 作为库ID使用
    """
    logger_plugin.debug('Start loading plugin [OfficialAccount] %s [Wechat] %s [Context] %s [Plugin] %s' % (
        official_account.__dict__,
        wechat.__dict__,
        context.__dict__,
        plugin.__dict__,
    ))

    if is_system:
        directory = os.path.join(settings.PROJECT_DIR, 'plugins/system')
    else:
        directory = os.path.join(settings.PROJECT_DIR, 'plugins')

    try:
        full_path = os.path.join(directory, plugin.iden)
        if not os.path.isdir(full_path):
            logger_plugin.warning('Plugin folder does not exist')
            raise PluginLoadError('Plugin folder does not exist')
        if not os.path.exists(os.path.join(full_path, 'process.py')):
            logger_plugin.warning('The process.py file does not exist in the plugins folder')
            raise PluginLoadError('The process.py file does not exist in the plugins folder')
    except OSError:
        logger_plugin.warning('Error when accessing plugin folder')
        raise PluginLoadError('Error when accessing plugin folder')

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
                    plugin_instance = plug(
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
                    logger_plugin.info('Finished loading plugin %s' % plug)
                    return plugin_instance
            else:
                if issubclass(plug, PluginProcessor):
                    plugin_instance = plug(
                        official_account=official_account,
                        wechat=wechat,
                        context=context,
                        message=message,
                        in_context=in_context,
                        is_exclusive=is_exclusive,
                        plugin=plugin,
                        is_system=is_system
                    )
                    logger_plugin.info('Finished loading plugin %s' % plug)
                    return plugin_instance
    logger_plugin.warning('You should set __all__ variable in process.py')
    raise PluginLoadError('You should set __all__ variable in process.py')