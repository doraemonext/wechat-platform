# -*- coding: utf-8 -*-

import logging

from system.plugin.framework import PluginProcessor

logger_plugins = logging.getLogger('plugins')

__all__ = ['PluginTest']


class PluginTest(PluginProcessor):
    """
    测试插件
    """
    def process(self):
        return self.wechat.send_template_message(
            user_id=self.message.source,
            template_id='HaBqpxp0FBaKF9eq1fxV6SpZTY0vV4I1Mm8I1pd-4WE',
            data={},
            url='http://www.baidu.com',
        )