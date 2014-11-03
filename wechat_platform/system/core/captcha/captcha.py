# -*- coding: utf-8 -*-

import requests


class Captcha(object):
    """
    验证码识别类
    """
    def __init__(self, file_path):
        self.file = open(file_path, 'rb').read()
        # TODO