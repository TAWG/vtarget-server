# -*- coding: utf-8 -*-
"""
   Description :
   Author :       sky
   date：          
"""
__author__ = 'sky'

import uuid
import hashlib
from common.common import wechat_config

prefix = 'vt_'


def generate_account():
    """
    账号生成方法
    :return:
    """
    uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, wechat_config['nameSpace']))
    return prefix + uid.replace("-", "")


def str_sign(src, sign='BjfCmLc'):
    """
    数据加密为md5
    :param src:
    :param sign:
    :return:
    """
    cur_md5 = hashlib.md5()
    cur_md5.update(('%s%s' % (src, sign)).encode("utf-8"))
    return cur_md5.hexdigest()
