# -*- coding: utf-8 -*-
"""
   Description :
   Author :       sky
   date：          
"""
__author__ = 'sky'

from common.transcation_manager import TranscationManager, transcation_manager
from common.local_cache import localCache
from common.constants import cache_conn_key
from exception.biz_exception import BizExcepition


def transcation(callback=Exception, required=transcation_manager.REQUIRE):
    """
    数据库事务装饰器 v1.0
    :param fun:
    :param kargs:
    :return:
    """
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            cur_transcation = None
            old_transcation = None
            is_first = True
            if required == TranscationManager.NOT_SUPPORT:
                if localCache.get_lcoal(cache_conn_key) is not None:
                    raise BizExcepition(9001, 'trancation error , %s not support transcation' % func.__name__)
                cur_transcation = transcation_manager.create_transcation()
            if required == TranscationManager.NEW:
                cur_transcation = transcation_manager.create_transcation()
                if localCache.get(cache_conn_key) is not None:
                    old_transcation = localCache.get(cache_conn_key)

            if required == TranscationManager.REQUIRE:
                if localCache.get(cache_conn_key) is not None:
                    is_first = False
                    cur_transcation = localCache.get(cache_conn_key)
                else:
                    cur_transcation = transcation_manager.create_transcation()
            try:
                localCache.set(cache_conn_key, cur_transcation)
                result = func(*args, **kwargs)
                if is_first:
                    transcation_manager.commit_transcation()
                return result
            except Exception as e:
                if callback in type(e).__bases__:
                    transcation_manager.rollback_transcation()
                else:
                    transcation_manager.commit_transcation()
                raise e
            finally:
                if required == TranscationManager.NEW and old_transcation is not None:
                    localCache.set(cache_conn_key, old_transcation)
                if is_first:
                    localCache.delete(cache_conn_key)

        return inner_wrapper

    return wrapper
