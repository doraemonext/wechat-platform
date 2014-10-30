# -*- coding: utf-8 -*-


class PluginProcessor(object):
    """
    插件响应过程基类, 每个插件响应过程都要在此基础上进行扩展
    """

    def __init__(self, *args, **kwargs):
        self.plugin = None
        self.official_account = None
        self.wechat = None
        self.message = None
        self.context = None
        self.in_context = False
        self.is_exclusive = False

    def init(self, plugin, official_account, wechat, message, context, in_context=False, is_exclusive=False):
        """
        初始化插件, 将状态信息存储
        :param plugin: 插件信息实例 (Plugin)
        :param official_account: 公众号实例 (OfficialAccount)
        :param wechat: 微信请求实例 (WechatBasic)
        :param message: 微信请求信息实例 (WechatMessage)
        :param context: 微信上下文对话实例 (DatabaseContextStore)
        :param in_context: 当前是否在上下文对话过程中
        :param is_exclusive: 插件是否可以独享响应内容
        """
        self.plugin = plugin
        self.official_account = official_account
        self.wechat = wechat
        self.message = message
        self.context = context
        self.in_context = in_context
        self.is_exclusive = is_exclusive

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

    def response_text(self, text):
        pass

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
        """ 响应函数, 由继承的类进行扩展, 当对本插件初始化完成后, 调用此函数即可得到响应结果 """
        raise NotImplementedError('subclasses of PluginProcess must provide an response() method')
