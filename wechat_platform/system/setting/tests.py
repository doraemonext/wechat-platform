# -*- coding: utf-8 -*-

from system.core.test import WechatTestCase
from system.setting.models import Setting


class SettingTest(WechatTestCase):
    def test_add_setting(self):
        """
        测试添加设置
        """
        init_sum = Setting.objects.count()
        setting_1 = Setting.manager.add('_name1', 'value1')
        setting_2 = Setting.manager.add('_name2', 'value2')
        setting_3 = Setting.manager.add('_name3', 'value3')
        self.assertEqual(init_sum + 3, Setting.objects.count())
        self.assertEqual(setting_1.name, '_name1')
        self.assertEqual(setting_1.value, 'value1')
        self.assertEqual(setting_2.name, '_name2')
        self.assertEqual(setting_2.value, 'value2')
        self.assertEqual(setting_3.name, '_name3')
        self.assertEqual(setting_3.value, 'value3')

    def test_add_repeat_setting(self):
        """
        测试添加重复设置
        """
        init_sum = Setting.objects.count()
        Setting.manager.add('_name1', 'value1')
        setting_1 = Setting.manager.add('_name1', 'value2')
        self.assertEqual(init_sum + 1, Setting.objects.count())
        self.assertEqual(setting_1.value, 'value1')
        setting_2 = Setting.manager.add('_name1', 'value3', force=True)
        self.assertEqual(init_sum + 1, Setting.objects.count())
        self.assertEqual(setting_2.value, 'value3')

    def test_get_setting(self):
        """
        测试获取单个设置
        """
        Setting.manager.add('_name1', 'value1')
        Setting.manager.add('_name2', 'value2')
        Setting.manager.add('_name3', 'value3')
        self.assertEqual('value1', Setting.manager.get('_name1'))
        self.assertEqual('value2', Setting.manager.get('_name2'))
        self.assertEqual('value3', Setting.manager.get('_name3'))

    def test_get_all_setting(self):
        """
        测试获取全部测试
        """
        Setting.manager.add('_name1', 'value1')
        Setting.manager.add('_name2', 'value2')
        Setting.manager.add('_name3', 'value3')
        result = Setting.manager.get_all()
        self.assertEqual(result['_name1'], 'value1')
        self.assertEqual(result['_name2'], 'value2')
        self.assertEqual(result['_name3'], 'value3')