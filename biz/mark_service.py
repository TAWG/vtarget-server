# -*- coding: utf-8 -*-
"""
   Description :
   Author :       sky
   date：          
"""
__author__ = 'sky'

import time
import datetime
from biz.base_service import BaseService
from biz.target_service import targetService
from biz.dict_service import dict_map
from exception.biz_exception import BizExcepition


class MarkService(BaseService):
    insert_sql = "insert into t_target_mark (u_id,t_id,count,mark_date) values (%s,%s,%s,'%s')"

    def add_mark(self, uid, tid, count):
        mark_date = time.strftime('%Y-%m-%d', time.localtime())
        if self.check_mark(uid, tid, mark_date) is False:
            raise BizExcepition(500, "今日已打卡")
        if count is None:
            target = targetService.get_target(tid)
            count = target['targetCount']

        self.db_pool.execute_insert_sql(
            self.insert_sql % (uid, tid, count, mark_date))

    def check_mark(self, uid, tid, mark_date):
        sql = "select * from t_target_mark where u_id = %s and t_id = %s and mark_date='%s'"
        marks = self.db_pool.execute_query_sql(sql % (uid, tid, mark_date), self.__query_parse)
        if len(marks) > 0:
            return False
        return True

    def get_marks(self, uid, check_date, page_no, page_size):
        sql = "select * from t_target_mark m left join t_user_target t  on m.t_id = t.id " \
              "where m.u_id = %s and m.mark_date between '%s' and '%s' limit %d,%d"
        start_index = self.page_helper(page_no, page_size)

        if check_date is None or len(check_date) == 0:
            start_date = datetime.date(datetime.date.today().year, datetime.date.today().month, 1)
            end_date = datetime.date(datetime.date.today().year, datetime.date.today().month + 1, 1)
        else:
            start_date = datetime.strptime(check_date, "%Y-%m")
            end_date = datetime.date(start_date.date.today().year, start_date.date.today().month + 1, 1)
        marks = self.db_pool.execute_query_sql(sql % (uid, start_date, end_date, start_index, 200),
                                               self.__query_parse)

        def marks_map(infos):
            res = {}
            for mark in infos:
                mark_date = mark['markDate'].split('-')[2]
                mark_type = mark['targetType']
                if mark_date not in res:
                    res[mark_date] = [mark_type]
                else:
                    if mark_type not in res[mark_date]:
                        res[mark_date].append(mark_type)
            return res

        return marks_map(marks)

    @staticmethod
    def __query_parse(result):
        res = []
        for row in result:
            tmp = dict()
            tmp['uid'] = row[1]
            tmp['tid'] = row[2]
            tmp['markDate'] = row[4]
            tmp['count'] = row[3]
            if len(row) > 10:
                tmp['targetType'] = dict_map[row[9]]
            res.append(tmp)
        return res


markService = MarkService()
