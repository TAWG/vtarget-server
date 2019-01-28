# -*- coding: utf-8 -*-
"""
   Description :  Mysql数据库连接池
   Author :       sky
   date：          
"""
__author__ = 'sky'

import DBUtils.PooledDB as dbUtil
from common.common import config
from app import logger
from exception.biz_exception import BizExcepition


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


db_pool = ConnectPool(config.load_db_config())

