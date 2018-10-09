# -*- coding: utf-8 -*-
"""
   Description :
   Author :       sky
   date：          
"""
__author__ = 'sky'

from flask import render_template, request, session, redirect
from biz.user_service import userService
import json


def index():
    form = request.values.to_dict()
    form = dict(form)
    context = {'title': form.get('test') if form.get('test') else '1'}
    return render_template("login.html", **context)


def login():
    form = request.values.to_dict()
    username = form['username']
    passwd = form['passwd']
    result = userService.signin(username, passwd)
    if result['code'] == 200:
        session['uid'] = result['data']['id']
        return redirect("/target/search")
    return json.dumps(result)


def signup_page():
    return render_template("signup.html")


def signup():
    form = request.values.to_dict()
    username = form['username']
    passwd = form['passwd']
    account = form['account']
    device_info = form.get("device_info") if form.get("device_info") is not None else {}
    result = userService.signup(account, username, passwd, **device_info)
    if result['code'] != 200:
        return json.dumps(result)
    return redirect("login.html")


def logout():
    session.pop['uid']
    return render_template("login.html")
