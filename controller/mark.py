# -*- coding: utf-8 -*-
"""
   Description :
   Author :       sky
   date：          
"""
__author__ = 'sky'

from biz.mark_service import markService
from app import session_check, json_result_warrper


@session_check
@json_result_warrper
def mark(**form):
    count = form.get('targetCount') if 'count' in form else None
    markService.add_mark(form['uid'], form['tid'], count)


@session_check
def search_mark():
    pass
