# -*- coding: utf-8 -*-
"""
   Description :
   Author :       sky
   date：          
"""
__author__ = 'sky'
import json
import os


class LoadConfig:
    """
    读取配置文件
    """

    config_file = "config.json"

    def __init__(self, other_config=None):
        if other_config is not None and type(other_config) == str:
            self.config_file = other_config
        with open(os.path.abspath(self.config_file)) as f:
            self.config = json.load(f)

    def load_all_config(self):
        return self.config

    def load_redis_config(self):
        if self.config is not None:
            return self.config["redis"]

    def load_login_config(self):
        if self.config is not None:
            return self.config["userInfo"]

    def load_db_config(self):
        if self.config is not None:
            return self.config["db"]

    def load_worker_config(self):
        if self.config is not None:
            return self.config["worker"]

    def load_config_by_key(self, key):
        if self.config is not None and key in self.config:
            return self.config[key]
        else:
            raise Exception("config error ")


config = LoadConfig()
db_config = config.load_db_config()
wechat_config = config.load_config_by_key('wechat')

