# -*- coding: utf-8 -*-

import uuid


def make_random_string():
    """
    生成32位随机字符串
    :return: 32位随机字符串
    """
    return uuid.uuid4().hex