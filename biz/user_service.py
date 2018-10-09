# -*- coding: utf-8 -*-
"""
   Description :
   Author :       sky
   date：          
"""
__author__ = 'sky'

from biz.base_service import BaseService
from util.util import generate_account
from exception.biz_exception import BizExcepition


class UserService(BaseService):
    """
    用户相关操作
    """
    get_user_sql = "select * from t_user_info where account = '%s' "
    insert_user_sql = "insert into t_user_info (account,username,passwd,can_update) values('%s','%s','%s',0)"

    def signin(self, username, passwd):
        result = {'code': 200, 'reason': 'success'}
        user = self.get_user(username)
        if user is None:
            raise BizExcepition(404,'用户不存在')
        if passwd != user['passwd']:
            raise BizExcepition(500, '用户名或密码错误')
        else:
            result["data"] = user
        return result

    def signup(self, account, username, passwd, **kwargs):
        user = self.get_user(account)
        if user is not None:
            raise BizExcepition(500, "用户已存在")
        self.db_pool.execute_insert_sql(self.insert_user_sql % (account, username, passwd))

    def wechat_signup(self, openId):
        sql = "insert into t_user_info (account,wechat,can_update) values ('%s','%s',1)"
        account = generate_account()
        self.db_pool.execute_insert_sql(sql % (account, openId))
        return self.get_user_by_openid(openId)

    def get_user_by_openid(self, openId):
        sql = "select * from t_user_info where wechat = '%s'"
        users = self.db_pool.execute_query_sql(sql % openId, self.__parse_user)
        return users[0]

    def get_user(self, username):
        users = self.db_pool.execute_query_sql(self.get_user_sql % username, self.__parse_user)
        if isinstance(users, list) and len(users) > 0:
            user = users[0]
            user['passwd'] = ''
            return users[0]
        return None

    def get_user_by_id(self, id):
        sql = "select * from t_user_info where id = '%s' "
        users = self.db_pool.execute_query_sql(sql % id, self.__parse_user)
        if isinstance(users, list) and len(users) > 0:
            user = users[0]
            user['passwd'] = ''
            return users[0]
        return None

    def update_user(self, info):
        pass

    @staticmethod
    def __parse_user(results):
        res = []
        for row in results:
            tmp = dict()
            tmp['id'] = row[0]
            tmp['userName'] = row[1]
            tmp['nickName'] = row[2]
            tmp['passwd'] = row[3]
            tmp['mail'] = row[4]
            tmp['canUpdate'] = row[6]
            tmp['sendFlag'] = row[7]
            res.append(tmp)
        return res


userService = UserService()
