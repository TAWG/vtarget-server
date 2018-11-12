# -*- coding: utf-8 -*-
"""
   Description :
   Author :       sky
   date：          
"""
__author__ = 'sky'

from common.mysql_client import db_pool


class BaseService:
    db_pool = db_pool

    @staticmethod
    def parse_count(result):
        row = result[0]
        if row is not None:
            return row[0]
        return 0

    @staticmethod
    def page_helper(page_no, page_size):
        start_index = 0
        if page_no > 1:
            start_index = (page_no - 1) * page_size
        return start_index

    def query_page(self, sql, page_size, start_index, processor):
        """
        统一分页处理
        :param sql: 执行的sql语句
        :param page_size: 每页大小
        :param start_index: 起始index
        :param processor: 返回值解析方法(func)
        :return:
        """
        total = self.query_count(sql)
        datas = list()
        if total > 0:
            sql += ' limit %s,%s' % (start_index, page_size)
            datas = self.db_pool.execute_query_sql(sql, processor)
        return {"total": total, "data": datas}

    def query_count(self, sql):
        """
        获取数量
        :param sql:
        :return:
        """
        start_index = sql.find("from")
        sql = "select count(1) %s" % sql[start_index:]
        return self.db_pool.execute_query_sql(sql, self.parse_count)
