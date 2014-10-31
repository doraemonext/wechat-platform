# -*- coding: utf-8 -*-

from system.plugin.framework import PluginProcessorSystem

__all__ = ['PluginSystemText']


class PluginSystemText(PluginProcessorSystem):
    def process(self):
        return 'test'