# -*- coding: utf-8 -*-
"""
   Description :
   Author :       sky
   date：          
"""
__author__ = 'sky'

import uuid
from common.common import wechat_config

prefix = 'vt_'


def generate_account():
    """
    账户生成方法
    :return:
    """
    uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, wechat_config['nameSpace']))
    return prefix + uid.replace("-", "")
