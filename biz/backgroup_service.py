# -*- coding: utf-8 -*-
"""
   Description :
   Author :       sky
   date：          
"""
__author__ = 'sky'

from biz.base_service import BaseService
from exception import biz_exception


class BackgroundService(BaseService):
    """
    后台管理服务逻辑类
    """

    def login(self, user_name, password):
        """
        管理用户登录
        :param user_name:
        :param password:
        :return:
        """
        sql = "select * from t_admin_user where username = '%s'"
        admin_users = self.db_pool.execute_query_sql(sql % user_name, self.__parse_admin_user)
        if admin_users is None or len(admin_users) == 0:
            raise biz_exception(404, 'admin user not exist')
        admin_user = admin_users[0]
        base_passwd = admin_user['passwd']
        if base_passwd != password:
            raise biz_exception(401, 'username or password error')
        return admin_user



    @staticmethod
    def __parse_admin_user(results):
        res = []
        for row in results:
            tmp = dict()
            tmp['id'] = row[0]
            tmp['userName'] = row[1]
            tmp['passwd'] = row[2]
            res.append(tmp)
        return res


backgroundService = BackgroundService()
