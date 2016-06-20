#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'pi'
__mtime__ = '8/23/2015-023'
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
import urllib.request, urllib.error, urllib.parse

# LOGIN_URL = r'http://www.zhihu.com/#signin'
URL_ROOT = r'http://d.weibo.com/#_loginLayer_1440327422006'
# LOGIN_URL = r'https://passport.csdn.net/account/login?ref=toolbar'

values = {'username': 'xingshang1992@163.com', 'password': '***********'}
data = urllib.parse.urlencode(values).encode()
# print(type(data), data)

user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
# user_agent = r'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
headers = {'User-Agent': user_agent}

request = urllib.request.Request(URL_ROOT, data, headers)
try:
    response = urllib.request.urlopen(request)
    page = response.read()
    print(page)
except urllib.error.URLError as e:
    print(e.reason)
