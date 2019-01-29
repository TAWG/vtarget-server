# -*- coding: utf-8 -*-
"""
   Description :
   Author :       sky
   date：          
"""
__author__ = 'sky'

from threading import local
from gevent.local import local as g_local


class BaseLocal:
    """
        缓存基础类
    """
    __slots__ = ["local_data"]

    def get(self, key):
        if hasattr(self.local_data, key):
            return self.local_data.__getattribute__(key)
        return None

    def set(self, key, value):
        self.local_data.__setattr__(key, value)

    def delete(self, key):
        self.local_data.__delattr__(key)


class ThreadLocal(BaseLocal):
    """
    线程安全缓存
    """
    __slots__ = ["local_data"]

    def __init__(self):
        self.local_data = local()


class CoroutineLocal(BaseLocal):
    """
    协程安全缓存
    """
    __slots__ = ["local_data"]

    def __init__(self):
        self.local_data = g_local()


localCache = CoroutineLocal()
