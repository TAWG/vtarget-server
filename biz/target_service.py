# -*- coding: utf-8 -*-
"""
   Description :
   Author :       sky
   date：          
"""
__author__ = 'sky'

from biz.base_service import BaseService
from exception.biz_exception import BizExcepition


class TargetService(BaseService):
    """
    微目标处理类
    """
    query_page_sql = 'select * from t_user_target where u_id = %s limit %s,%s'
    query_target_sql = 'select * from t_user_target where id = %s'

    def get_targets(self, uid, page_no=1, page_size=5):
        """
        分页获取用户微目标
        :param uid:
        :param page_no:
        :param page_size:
        :return:
        """
        start_index = self.page_helper(page_no, page_size)
        targets = self.db_pool.execute_query_sql(self.query_page_sql % (uid, start_index, page_size),
                                                 self.__parse_target)
        return targets

    def add_target(self, target_info):
        """
        添加微目标
        :param target_info:
        :return:
        """
        try:
            if self.count_target(target_info['uid']) >= 5:
                raise BizExcepition(500, "微目标最多只能设定5个")
            sql = "insert into  t_user_target (u_id,target_type,target_content,target_count) " \
                  "values ('%s','%s','%s','%s')"
            self.db_pool.execute_insert_sql(sql % (
                target_info['uid'], target_info['targetType'], target_info['targetContent'],
                target_info['targetCount']))
        except Exception as e:
            return False
        return True

    def count_target(self, uid):
        """
        获取用户下微目标数
        :param uid:
        :return:
        """
        sql = "select count(1) from t_user_target where u_id = %s"
        count = self.db_pool.execute_query_sql(sql % uid, self.parse_count)
        return count if count is not None else 0

    def del_target(self, target_id):
        pass

    def get_target(self, t_id):
        """
        通过ID获取微目标
        :param t_id:
        :return:
        """
        targets = self.db_pool.execute_query_sql(self.query_target_sql % t_id, self.__parse_target)
        return targets[0]

    @staticmethod
    def __parse_target(results):
        """
        数据库解析方法
        :param results:
        :return:
        """
        res = []
        for row in results:
            tmp = dict()
            tmp['id'] = row[0]
            tmp['uid'] = row[1]
            tmp['targetType'] = row[2]
            tmp['targetContent'] = row[3]
            tmp['targetCount'] = row[4]
            res.append(tmp)
        return res


targetService = TargetService()
