# -*- coding: utf-8 -*-
"""
   Description :
   Author :       sky
   date：          
"""
__author__ = 'sky'

import flask
import json
import os
import functools
import time
import logging
from inspect import isfunction
from datetime import timedelta
from exception.biz_exception import BizExcepition
from common.common import config


app = flask.Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
logger = app.logger


def config_log():
    """
    日志配置
    :return:
    """
    app_config = config.load_config_by_key("app")
    file_name = app_config.get('logName') if app_config.get("logName") else "logger"
    log_path = app_config.get('logPath')

    def make_dir(make_dir_path):
        path = make_dir_path.strip()
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    log_dir_name = "logs"
    log_file_name = file_name + '-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
    log_file_folder = os.path.abspath(
        os.path.join(os.path.dirname(log_path), os.pardir, os.pardir)) + os.sep + log_dir_name
    make_dir(log_file_folder)
    log_file_str = log_file_folder + os.sep + log_file_name
    log_level = logging.INFO

    handler = logging.FileHandler(log_file_str, encoding='UTF-8')
    handler.setLevel(log_level)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def route_parse(routes):
    """
    将配置文件解析为路由信息
    :param routes:
    :return:
    """
    for path, pack in routes.items():
        option = {"methods": ['get', 'post']}
        info_list = pack.split('.')
        p_index = pack.rfind('.')
        obj = __import__(pack[:p_index])
        for info in info_list[1:]:
            if hasattr(obj, info):
                obj = getattr(obj, info)
        if isfunction(obj):
            if obj.__name__ == 'wrapper':
                obj = getattr(obj, info)
            app.add_url_rule(path, obj.__name__, obj, **option)
            logger.info("load url %s add to route" % path)
        else:
            raise Exception("config error ,%s is not function" % pack)


def json_result_warrper(func):
    """
    Json结果处理装饰器
    :param func:
    :param need_session:
    :return:
    """

    @functools.wraps(func)
    def wrapper(**kargs):
        res = {"code": 200, "reason": "success"}
        url = flask.request.url
        form = flask.request.values.to_dict()
        logger.info("request %s,param %s" % (url, form))
        if 'uid' in kargs:
            uid = kargs['uid']
            form['uid'] = uid
        try:
            result = func(**form)
            if result is not None:
                res['data'] = result
        except BizExcepition as be:
            res['code'] = be.code
            res['reason'] = be.reason
            logger.error("request %s error %s" % (url, be))
        except Exception as e:
            res['code'] = 500
            res['reason'] = '服务器开小差了'
            logger.error("request %s error %s" % (url, e))
        return json.dumps(res)

    return wrapper


def session_check(func):
    """
    session信息拦截器
    :param func:
    :return:
    """

    @functools.wraps(func)
    def wrapper():
        if 'uid' not in flask.session:
            return json.dumps({'code': 401, 'reason': '未登录'})
        form = flask.request.values.to_dict()
        form['uid'] = flask.session['uid']
        return func(**form)

    return wrapper


if __name__ == '__main__':
    config_log()
    with open('route.json') as f:
        route_info = json.load(f)
        routes = route_info['route']
        route_parse(routes)
    app.run(host="0.0.0.0")
