# -*- coding: utf-8 -*-
"""
   Description :  gevent wsgi拉起应用
   Author :       sky
   date：          
"""
__author__ = 'sky'

import app
import json
from gevent.pywsgi import WSGIServer
from common.common import config


port = config.config.get("app").get("port")
if port is None or type(port) != int or port > 65535 or port < 1:
    port = 80
app.config_log()
with open('route.json') as f:
    route_info = json.load(f)
    routes = route_info['route']
    app.route_parse(routes)
http_server = WSGIServer(('', port), app.app)
http_server.serve_forever()
