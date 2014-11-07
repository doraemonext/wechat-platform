# -*- coding: utf-8 -*-

import logging
import random
from xml.dom import minidom
from xml.parsers.expat import ExpatError

from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
from wechat_sdk.context.framework.django import DatabaseContextStore
from wechat_sdk.messages import EventMessage

from system.core.exceptions import WechatCriticalException
from system.rule.models import Rule
from system.keyword.models import Keyword
from system.rule_match.models import RuleMatch
from system.request.models import RequestMessage, RequestEvent
from system.response.models import Response
from system.plugin import PluginLoadError, PluginException, PluginResponseError
from system.plugin.models import Plugin
from system.plugin.framework import load_plugin
from system.setting.models import Setting

logger_control = logging.getLogger(__name__)


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

        self.match_plugin_list = []

    def match(self):
        """
        对微信请求信息进行匹配, 设置匹配的插件标识符
        """
        # 如果当前在上下文对话模式中, 直接返回该插件iden
        context_plugin_iden = self.context.get('_plugin_iden')
        if context_plugin_iden:
            return [{
                'iden': context_plugin_iden,
                'reply_id': 0
            }, ]

        # 如果不在上下文对话模式中, 直接匹配信息类型, 然后转发给响应的详细匹配函数并返回结果
        if isinstance(self.message, EventMessage):
            func = 'match_event'
        else:
            func = 'match_' + self.message.type
        if hasattr(self, func):
            return getattr(self, func)()
        else:
            logger_control.error('No method matched [OfficialAccount] %s [Wechat] %s [Message] %s [Context] %s' % (
                self.official_account.__dict__,
                self.wechat.__dict__,
                self.message.__dict__,
                self.context.__dict__,
            ))
            raise WechatCriticalException('No method matched')

    def match_event(self):
        """
        对事件请求信息进行匹配, 并返回匹配的插件标识符列表
        :return: 插件标识符列表, 格式描述参见 __init__ 函数
        """
        if self.message.type == 'subscribe':  # 当为关注事件时
            rule = Rule.objects.get(name='_system_subscribe_' + self.official_account.iden)
            rule_match = RuleMatch.manager.get(rule=rule)
            plugin_list = []
            for item in rule_match:
                plugin_list.append({
                    'iden': item.plugin_iden,
                    'reply_id': item.reply_id
                })
            return self._arrange_plugin_list(rule, plugin_list)
        elif self.message.type == 'unsubscribe':  # 当取消关注时, 什么也不做
            return []
        elif self.message.type == 'click':
            self.message.content = self.message.key  # 将 key 值转换为 content 后直接使用文本信息的匹配
            return self.match_text()
        elif self.message.type == 'view':  # 当页面跳转事件发生时, 什么也不做
            return []
        elif self.message.type == 'location':  # 当地理位置上报时, 什么也不做
            return []
        else:
            return self._get_default_list()

    def match_text(self):
        """
        对文本请求信息进行匹配, 并返回匹配的插件标识符列表
        :return: 插件标识符列表, 格式描述参见 __init__ 函数
        """
        keyword = Keyword.manager.search(official_account=self.official_account, keyword=self.message.content)
        if not keyword:  # 当没有找到匹配关键字时返回默认回复插件
            return self._get_default_list()

        rule = keyword.rule
        rule_match = RuleMatch.manager.get(rule=rule)
        if not rule_match:  # 当该规则没有任何插件匹配可以使用时返回默认回复插件
            return self._get_default_list()

        # 将该规则所有的插件匹配按顺序写入列表
        plugin_list = []
        for item in rule_match:
            plugin_list.append({
                'iden': item.plugin_iden,
                'reply_id': item.reply_id
            })

        return self._arrange_plugin_list(rule, plugin_list)

    def process(self, plugin_dict, is_exclusive=False):
        """
        插件处理过程, 负责调用插件并返回执行结果
        :param plugin_dict: 插件字典, exp: {'iden': 'plugin_iden', 'reply_id': 0}
        :param is_exclusive: 插件是否可以独享该操作
        :return: 插件返回结果
        """
        iden = plugin_dict['iden']
        reply_id = plugin_dict['reply_id']

        if self._is_system_plugin(iden=iden):
            plugin = Plugin(iden=iden, name=iden)
        else:
            plugin = Plugin.manager.get(official_account=self.official_account, iden=iden)

        plugin_loaded = load_plugin(
            official_account=self.official_account,
            wechat=self.wechat,
            context=self.context,
            message=self.message,
            is_exclusive=is_exclusive,
            plugin=plugin,
            reply_id=reply_id,  # 仅系统插件可用
            is_system=self._is_system_plugin(iden)
        )
        return plugin_loaded.process()

    @property
    def response(self):
        final_response = None

        # 判断请求是否重复, 如果重复则返回原响应内容, 否则保存当前请求
        if isinstance(self.message, EventMessage):
            if RequestEvent.manager.is_repeat(official_account=self.official_account, wechat_instance=self.wechat):
                # TODO: return the response
                raise Exception('have not yet implemented')
            RequestEvent.manager.add(official_account=self.official_account, wechat_instance=self.wechat)
        else:
            if RequestMessage.manager.is_repeat(official_account=self.official_account, wechat_instance=self.wechat):
                responses = Response.manager.get(official_account=self.official_account, msgid=self.message.id)
                if responses:  # 当数据库中已经存在对于该请求的回复时
                    result = None
                    for response in responses:
                        if response.pattern == Response.PATTERN_NORMAL:
                            result = response.raw
                            break
                    if result:
                        return HttpResponse(result)
                    else:
                        return HttpResponse('')
                else:  # 当数据库中不存在对于该请求的回复时
                    if Response.manager.is_waiting(official_account=self.official_account, wechat_instance=self.wechat):
                        return HttpResponse('')
            RequestMessage.manager.add(official_account=self.official_account, wechat_instance=self.wechat)

        self.match_plugin_list = self.match()
        if len(self.match_plugin_list) == 0:  # 当该请求不需要插件响应时, 直接回复空字符串
            return HttpResponse('')
        elif len(self.match_plugin_list) == 1:  # 当只需要单个插件响应时, 可以独享操作
            is_exclusive = True
        elif len(self.match_plugin_list) > 1:  # 当需要多个插件响应时, 不可以独享
            is_exclusive = False
            Response.manager.add_waiting(official_account=self.official_account, wechat_instance=self.wechat)

        for plugin in self.match_plugin_list:
            try:
                result = self.process(plugin_dict=plugin, is_exclusive=is_exclusive)
                if result and is_exclusive:  # 说明该插件需要返回XML数据
                    Response.manager.add(official_account=self.official_account, wechat_instance=self.wechat,
                                         type=self._analyse_response_type(result), pattern=Response.PATTERN_NORMAL,
                                         raw=result, plugin_dict=plugin)
                    final_response = result
                else:  # 说明该插件不需要返回XML数据, 已经自行处理完成, 返回空字符串即可
                    final_response = ''
            except PluginResponseError, e:
                logger_control.warning('The plugin \'%s\' doesn\'t know how to response [Exception: %s]' % (plugin['iden'], e))
                final_response = self.wechat.response_text(Setting.manager.get('unknown_response'))
                break
            except PluginException, e:
                logger_control.error('The plugin \'%s\' response error [Exception: %s]' % (plugin['iden'], e))
                pass
        Response.manager.end_waiting(official_account=self.official_account, wechat_instance=self.wechat)

        self.context.save()  # 保存所有上下文对话到数据库中
        return HttpResponse(final_response)

    def _arrange_plugin_list(self, rule, plugin_list):
        """
        根据Rule中的返回模式重新组织插件列表
        :param rule: 规则实例 (Rule)
        :param plugin_list: 插件列表
        :return: 组织好的插件列表
        """
        plugin_list_len = len(plugin_list)

        if rule.reply_pattern == Rule.REPLY_PATTERN_ALL:  # 全部回复
            return plugin_list
        elif rule.reply_pattern == Rule.REPLY_PATTERN_RANDOM:  # 随机回复
            return [random.choice(plugin_list), ]
        elif rule.reply_pattern == Rule.REPLY_PATTERN_FORWARD:  # 顺序回复
            response_history = Response.manager.get_latest(official_account=self.official_account, wechat_instance=self.wechat)
            if response_history:
                try:
                    index = plugin_list.index({
                        'iden': response_history[0].plugin_iden,
                        'reply_id': response_history[0].reply_id,
                    })
                    if index == plugin_list_len - 1:
                        return [plugin_list[0], ]
                    return [plugin_list[index+1], ]
                except ValueError:
                    return [plugin_list[0], ]
            else:
                return [plugin_list[0], ]
        elif rule.reply_pattern == Rule.REPLY_PATTERN_REVERSE:  # 逆序回复
            response_history = Response.manager.get_latest(official_account=self.official_account, wechat_instance=self.wechat)
            if response_history:
                try:
                    index = plugin_list.index({
                        'iden': response_history[0].plugin_iden,
                        'reply_id': response_history[0].reply_id,
                    })
                    if index == 0:
                        return [plugin_list[plugin_list_len-1], ]
                    return [plugin_list[index-1], ]
                except ValueError:
                    return [plugin_list[plugin_list_len-1], ]
            else:
                return [plugin_list[plugin_list_len-1], ]

    def _analyse_response_type(self, xml):
        """
        分析返回XML的类型
        :param xml: 返回数据的XML
        :return: 类型
        """
        result = {}

        try:
            doc = minidom.parseString(xml.encode('utf-8'))
        except ExpatError:
            return {}
        params = [ele for ele in doc.childNodes[0].childNodes if isinstance(ele, minidom.Element)]
        for param in params:
            if param.childNodes:
                result[param.tagName] = param.childNodes[0].data

        return result['MsgType']

    def _get_default_list(self):
        """
        返回默认回复的插件 iden 及 reply_id 所组成的列表
        :return: 列表
        """
        rule = Rule.objects.get(name='_system_default_' + self.official_account.iden)
        rule_match = RuleMatch.manager.get(rule=rule)
        plugin_list = []
        for item in rule_match:
            plugin_list.append({
                'iden': item.plugin_iden,
                'reply_id': item.reply_id
            })

        return self._arrange_plugin_list(rule, plugin_list)

    def _is_system_plugin(self, iden):
        """
        根据 iden 判定是否为系统插件
        :param iden: 插件标识符
        :return: 如果为系统插件, 返回 True
        """
        system_plugin = [
            'text',
            'news',
            'music',
            'picture',
            'video',
            'voice',
            'location',
            'link',
            'default',
            'subscribe',
            'unsubscribe',
            'click',
            'view'
        ]
        if iden in system_plugin:
            return True
        else:
            return False