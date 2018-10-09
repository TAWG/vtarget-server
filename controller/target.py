# -*- coding: utf-8 -*-
"""
   Description :
   Author :       sky
   date：          
"""
__author__ = 'sky'

from flask import render_template
from app import session_check
from biz.target_service import targetService


@session_check
def add_target(**form):
    targetService.add_target(form)
    targets = targetService.get_targets(form['uid'], 1, 5)
    results = {"targets": targets}
    return render_template('target.html', **results)


@session_check
def search_target(**form):
    targets = targetService.get_targets(form['uid'], 1, 5)
    results = {"targets": targets}
    return render_template('target.html', **results)


