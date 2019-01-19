# -*- coding: utf-8 -*-
"""
   Description :  Mysql数据库连接池
   Author :       sky
   date：          
"""
__author__ = 'sky'

import DBUtils.PooledDB as dbUtil
import threading
from common.common import config
from app import logger
from exception.biz_exception import BizExcepition

local = threading.local()


def get_local(self):
    return self.local.conn


def set_local(self, conn):
    self.local.conn = conn


def del_local(self):
    del self.local.conn

def transcation(fun, **kargs):
    """
    数据库事务装饰器 v1.0
    :param fun:
    :param kargs:
    :return:
    """
    def wrapper(*args, **kw):
        callback = kargs.get("callback", Exception)
        require = kargs.get("require", TranscationManager.REQUIRE)
        cur_transcation = None
        old_transcation = None
        is_first = True
        if require == TranscationManager.NOT_SUPPORT:
            if transcation_manager.get_lcoal() is not None:
                raise BizExcepition(9001, 'trancation error , %s not support transcation' % fun.__name__)
            cur_transcation = transcation_manager.create_transcation()
        if require == TranscationManager.NEW:
            cur_transcation = transcation_manager.create_transcation()
            if transcation_manager.get_local() is not None:
                old_transcation = transcation_manager.get_local()
        if require == TranscationManager.REQUIRE:
            if transcation_manager.get_local() is not None:
                is_first = False
                cur_transcation = transcation_manager.get_lcoal()
            else:
                cur_transcation = transcation_manager.create_transcation()
        try:
            transcation_manager.set_local(cur_transcation)
            fun(*args, **kw)
            if is_first:
                transcation_manager.commit_transcation()
        except Exception as e:
            if callback in type(e).__bases__:
                transcation_manager.rollback_transcation()
            else:
                transcation_manager.commit_transcation()
            raise e
        finally:
            if require == TranscationManager.NEW and old_transcation is not None:
                transcation_manager.set_local(old_transcation)
            if is_first:
                transcation_manager.del_local()


class ConnectPool:
    """
    数据库连接池
    """

    def __init__(self, db_config):
        if db_config is None:
            raise Exception("load config error")
        self.creator = __import__(db_config["creator"])
        self.host = db_config['host']
        self.port = int(db_config['port'])
        self.passwd = db_config['password']
        self.username = db_config['username']
        self.db = db_config['db']
        self.pool = dbUtil.PooledDB(creator=self.creator, host=self.host, port=self.port,
                                    user=self.username, password=self.passwd, db=self.db)

    def get_conn(self):
        return self.pool.connection()

    def execute_query_sql(self, sql, process):
        try:
            conn = self.get_conn()
            cur = conn.cursor()
            logger.info("process sql : %s" % sql)
            cur.execute(sql)
            results = cur.fetchall()
            return process(results)
        except Exception as e:
            logger.error("sql error :%s" % e)
            raise BizExcepition(500, "DB Error")
        finally:
            cur.close()

    @transcation
    def execute_sql(self, sql):
        conn = self.get_conn()
        cur = conn.cursor()
        logger.info("execute sql : %s" % sql)
        cur.execute(sql)

    def execute_insert_sql(self, sql):
        conn = self.get_conn()
        try:
            cur = conn.cursor()
            logger.info("execute sql : %s" % sql)
            cur.execute(sql)
        except Exception as e:
            conn.rollback()
            logger.error("process sql : %s,error : %s" % (sql, e))
            raise BizExcepition(500, "DB Error")
        else:
            conn.commit()  # 事务提交
            print('事务处理成功', cur.rowcount)


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
        conn = self.get_local()
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
        conn = self.get_local()
        if conn is not None:
            try:
                conn.rollback()
            except Exception as e:
                raise e
            finally:
                conn.close()
        else:
            raise TypeError


db_pool = ConnectPool(config.load_db_config())
transcation_manager = TranscationManager(db_pool)
