# -*- coding: utf-8 -*-
"""
   Description :
   Author :       sky
   date：          
"""
__author__ = 'sky'

from threading import local


class ThreadLocal():
    local_data = local()

    def __init__(self):
        self.local_data = local()

    def get(self, key):
        if hasattr(self.local_data,key):
            return self.local_data.__getattribute__(key)
        return None

    def set(self, key, value):
        self.local_data.__setattr__(key, value)

    def delete(self, key):
        self.local_data.__delattr__(key)

threadLocal = ThreadLocal()
