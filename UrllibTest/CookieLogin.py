#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'pi'
__mtime__ = '8/23/2015-023'
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

LOGIN_URL = 'http://www.jobbole.com/wp-admin/admin-ajax.php'
get_url = 'http://www.jobbole.com/'  # 利用cookie请求访问另一个网址

values = {'action': 'user_login', 'user_login': 'pipiyn', 'user_pass': '****'}
postdata = urllib.parse.urlencode(values).encode()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'}

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
for item in cookie_jar:
    print('Name = ' + item.name)
    print('Value = ' + item.value)

get_request = urllib.request.Request(get_url, headers=headers)
get_response = opener.open(get_request)
print('个人主页' in get_response.read().decode())
