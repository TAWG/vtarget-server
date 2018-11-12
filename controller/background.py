# -*- coding: utf-8 -*-
"""
   Description :
   Author :       sky
   date：          
"""
__author__ = 'sky'
from flask import render_template, request
from app import check_back_session
from biz.backgroup_service import backgroundService


def backgroup_index():
    context = {}
    return render_template("back_index.html", **context)


def backgroup_login():
    form = request.values.to_dict()
    return render_template("back_index.html", **form)

@check_back_session
def add_banner():
    pass
