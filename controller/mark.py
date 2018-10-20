# -*- coding: utf-8 -*-
"""
   Description :
   Author :       sky
   date：          
"""
__author__ = 'sky'

from biz.mark_service import markService
from common.common import config
from app import session_check, json_result_warrper

max_target = config.load_config_by_key("app")['maxTarget']


@session_check
@json_result_warrper
def mark(**form):
    count = form.get('targetCount') if 'count' in form else None
    markService.add_mark(form['uid'], form['tid'], count)


@session_check
@json_result_warrper
def search_mark(**form):
    return markService.get_marks(form.get['uid'], form.get['date'], 1, max_target * 31)

