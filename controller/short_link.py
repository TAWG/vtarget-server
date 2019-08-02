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
import hashlib


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


def link_custom_page():
    return render_template('link_custom.html')


def short_link_custom():
    form = req.values.to_dict()
    form = dict(form)
    base_url = form['base_url']
    src_url = parse.quote(base_url)
    mid_url = form['mid_url']


    with request.urlopen(
            "http://api.t.sina.com.cn/short_url/shorten.json?source=3271760578&url_long=%s" % src_url) as f:
        data = f.read()
        data = json.loads(data.decode())
        short_url = data[0]['url_short'][7:]
    s = "%s_%s_%s" % (short_url, 'demo', 'test')
    m = hashlib.md5()
    m.update(s.encode("utf-8"))
    sign = m.hexdigest()
    build_url = "%s?clickUrl=%s&partner_code=demo&partner_key=test&type=2&token=%s" % (mid_url,short_url,sign)
    with request.urlopen(
            "http://api.t.sina.com.cn/short_url/shorten.json?source=3271760578&url_long=%s" % parse.quote(build_url)) as f:
        data = f.read()
        data = json.loads(data.decode())
        results = {"short_url": data[0]['url_short'],"base_url":base_url,"mid_url":mid_url}
        return render_template('link_custom.html', **results)



