# -*- coding: utf-8 -*-
"""
   Description :
   Author :       sky
   date：          
"""
__author__ = 'sky'


class BizExcepition(Exception):
    """
    业务异常
    """
    code = 500
    reason = None

    def __init__(self, reason):
        self.reason = reason

    def __init__(self, code, reason):
        self.code = code
        self.reason = reason
