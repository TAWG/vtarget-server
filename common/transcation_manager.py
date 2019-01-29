# -*- coding: utf-8 -*-
"""
   Description :
   Author :       sky
   date：          
"""
__author__ = 'sky'

from common.mysql_client import ConnectPool, db_pool
from common.local_cache import localCache


class TranscationManager:
    """
    事务管理实现
    """

    NEW = 0
    REQUIRE = 1
    NOT_SUPPORT = 2

    def __init__(self, data_source):
        if isinstance(data_source, ConnectPool):
            self.data_source = data_source

    def create_transcation(self):
        return self.data_source.get_conn()

    def commit_transcation(self):
        conn = localCache.get("conn")
        if conn is not None:
            try:
                conn.commit()

            except Exception as e:
                raise e
            finally:
                conn.close()
        else:
            raise TypeError

    def rollback_transcation(self):
        conn = localCache.get("conn")
        if conn is not None:
            try:
                conn.rollback()
            except Exception as e:
                raise e
            finally:
                conn.close()
        else:
            raise TypeError


transcation_manager = TranscationManager(db_pool)
