#!/usr/bin/env python
# encoding: utf-8
"""
@author: sky
@file: short_link.py
@time: 2019/7/28 0:16
@desc:
"""

__author__ = 'sky'
from urllib import request,parse
from flask import request as req,render_template
import json


def link_page():
    return render_template('link.html')


def short_link():
    form = req.values.to_dict()
    form = dict(form)
    long_url = form['url']
    src_url = parse.quote(long_url)
    with request.urlopen(
            "http://api.t.sina.com.cn/short_url/shorten.json?source=3271760578&url_long=%s" % src_url) as f:
        data = f.read()
        data = json.loads(data.decode())
        print(data)
        results = {"short_url": data[0]['url_short'],"src_url":data[0]['url_long']}
        return render_template('link.html', **results)
