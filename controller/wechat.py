# -*- coding: utf-8 -*-
"""
   Description :
   Author :       sky
   date：          
"""
__author__ = 'sky'
import json
import urllib.request as http_clinet
import ssl

from app import json_result_warrper, session_check
from common.common import wechat_config
from exception.biz_exception import BizExcepition
from flask import request, session
from biz.mark_service import markService
from biz.target_service import targetService
from biz.user_service import userService
from biz.dict_service import dict_map


@session_check
@json_result_warrper
def wechat_mark(**form):
    count = form.get('count') if 'count' in form else None
    if 'uid' not in form or 'tid' not in form:
        raise BizExcepition(101, '参数错误')
    markService.add_mark(form['uid'], form['tid'], count)


@session_check
@json_result_warrper
def wechat_mark_search(**form):
    marks = markService.get_marks(form['uid'], form.get("date"), 1, 5)
    return marks


@session_check
@json_result_warrper
def wechat_target_search(**form):
    targets = targetService.get_targets(form['uid'], 1, 5)
    return targets


@session_check
@json_result_warrper
def wechat_target_detail(**form):
    target = targetService.get_target(form['id'])
    return target

@session_check
@json_result_warrper
def wechat_target_add(**form):
    targetService.add_target(form)

@json_result_warrper
def wechat_target_type():
    return dict_map


@session_check
@json_result_warrper
def wechat_user_info(**form):
    user = userService.get_user(form['uid'])
    return user


def wechat_login():
    result = {'code': 200, 'reason': 'success'}
    url = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code"
    ssl._create_default_https_context = ssl._create_unverified_context
    form = request.values.to_dict()
    code = form['code']
    with http_clinet.urlopen(url % (wechat_config['appId'], wechat_config['appSecret'], code)) as req:
        data = json.loads(bytes.decode(req.read()))
        if 'openid' in data:
            open_id = data['openid']
            user = userService.get_user_by_openid(open_id)
            session_key = data["session_key"]
            if user is None:
                user = userService.wechat_signup(open_id)
            session["uid"] = user['id']
            session["sessionKey"] = session_key
        else:
            result['code'] = 401
            result['reason'] = "请重新授权"
        return json.dumps(result)
