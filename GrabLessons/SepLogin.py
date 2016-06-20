#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = '皮'
__mtime__ = '9/17/2015-017'
__email__ = 'pipisorry@126.com'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""

import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
import re
import requests

LOGIN_URL = 'http://sep.ucas.ac.cn/slogin'
PORTAL_SITE_URL = r'http://sep.ucas.ac.cn/portal/site/226/821'
# get_url = 'http://sep.ucas.ac.cn/appStore'
# get_url = 'http://jwjz.ucas.ac.cn/Student/DeskTopModules/bottomFrame.aspx'
STUDENT_URL = 'http://jwjz.ucas.ac.cn/Student/'  # 利用cookie请求访问另一个网址

values = {'userName': 'piting15@mails.ucas.ac.cn', 'pwd': '******************', 'sb': 'sb'}
postdata = urllib.parse.urlencode(values).encode()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 '
                  'Safari/537.36'}

cookie_filename = 'cookie_jar.txt'
cookie_jar = http.cookiejar.MozillaCookieJar(cookie_filename)
handler = urllib.request.HTTPCookieProcessor(cookie_jar)
opener = urllib.request.build_opener(handler)

request = urllib.request.Request(LOGIN_URL, postdata, headers)
try:
    response = opener.open(request)
    # print(response.read().decode())
except urllib.error.URLError as e:
    print(e.code, ':', e.reason)

cookie_jar.save(ignore_discard=True, ignore_expires=True)  # 保存cookie到cookie.txt中
# for item in cookie_jar:
#     print("%s:%s" % (item.name, item.value))

get_request = urllib.request.Request(PORTAL_SITE_URL, headers=headers)
get_response = opener.open(get_request)
new_login_url = re.search(r'http-equiv=\"refresh\".*?url=(.*?)\">', get_response.read().decode()).group(1)
# print(new_login_url)
# for item in cookie_jar:
#     print("%s:%s" % (item.name, item.value))


get_request = urllib.request.Request(new_login_url, headers=headers)
opener.open(get_request)
# for item in cookie_jar:
#     print("%s:%s" % (item.name, item.value))

get_request = urllib.request.Request(STUDENT_URL, headers=headers)
get_response = opener.open(get_request)

print(get_response.read().decode())
