# -*- coding: utf-8 -*-

import uuid
import os
import string
import random


def make_unique_random_string():
    """
    生成32位随机字符串, UUID
    :return: 32位随机字符串
    """
    return uuid.uuid4().hex


def make_random_string(length=32, integer=False):
    """
    生成长度为 length 的随机字符串
    :param length: 随机字符串长度
    :return: 指定长度的随机字符串
    """
    if integer:
        return ''.join(random.choice(string.digits) for i in range(length))
    else:
        return ''.join(random.choice(string.ascii_letters+string.digits) for i in range(length))
