# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.db.models.signals import post_migrate

from system.setting.models import Setting


def init_setting_table(sender, **kwargs):
    Setting.manager.add('title', u'微信公众平台管理系统')
    Setting.manager.add('description', u'微信公众平台管理系统')
    Setting.manager.add('captcha_ruokuai_username', '')
    Setting.manager.add('captcha_ruokuai_password', '')
    Setting.manager.add('captcha_ruokuai_typeid', '3040')
    Setting.manager.add('captcha_ruokuai_timeout', '60')
    # 下面两项为我(Doraemonext)在若快开发者账号中新建的ID和KEY, 可以在后台管理界面中更改
    Setting.manager.add('captcha_ruokuai_softid', '27197')
    Setting.manager.add('captcha_ruokuai_softkey', '564a64b2a62e49de9f492a43ae3cf8c5')
    Setting.manager.add('unknown_response', u'无法匹配到您的用户身份，请重新发送您刚才的信息')


class SettingAppConfig(AppConfig):
    name = 'system.setting'

    def ready(self):
        post_migrate.connect(init_setting_table, sender=self)