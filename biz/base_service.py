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
