# -*- coding: utf-8 -*-
"""
   Description :
   Author :       sky
   date：          
"""
__author__ = 'sky'
from biz.base_service import BaseService


class DictService(BaseService):
    type_list = []

    sql = "select * from t_vtarget_dict where type = %d order by type "

    def __init__(self):
        self.type_list = self.db_pool.execute_query_sql(self.sql % 1, self.__parse)

    @staticmethod
    def __parse(result):
        res = []
        for row in result:
            tmp = dict()
            tmp['type'] = row[2]
            tmp['name'] = row[1]
            tmp['image'] = row[4]
            res.append(tmp)
        return res


dict_map = DictService().type_list
