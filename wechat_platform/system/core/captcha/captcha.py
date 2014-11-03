# -*- coding: utf-8 -*-

import json
import requests

from system.core.captcha.utils import CaptchaException
from system.setting.models import Setting


class Captcha(object):
    """
    验证码识别类
    """
    def __init__(self, file_path):
        settings = Setting.manager.get_all()
        self.__username = settings['captcha_ruokuai_username']
        self.__password = settings['captcha_ruokuai_password']
        self.__typeid = settings['captcha_ruokuai_typeid']
        self.__timeout = settings['captcha_ruokuai_timeout']
        self.__softid = settings['captcha_ruokuai_softid']
        self.__softkey = settings['captcha_ruokuai_softkey']
        self.__file = open(file_path, 'rb').read()

    def recognition(self):
        """
        获取验证码识别结果
        :return: 验证码识别结果字符串
        :raise CaptchaException: 当验证码识别过程出错时抛出
        """
        url = 'http://api.ruokuai.com/create.json'
        payload = {
            'username': self.__username,
            'password': self.__password,
            'typeid': self.__typeid,
            'timeout': self.__timeout,
            'softid': self.__softid,
            'softkey': self.__softkey,
        }
        files = {
            'image': self.__file,
        }
        r = requests.post(url, data=payload, files=files)

        try:
            return json.loads(r.text)['Result']
        except (KeyError, ValueError):
            raise CaptchaException(r.text)
