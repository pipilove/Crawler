#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'pi'
__mtime__ = '8/26/2015-026'
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
import urllib.request, urllib.parse, http.cookiejar


def login():  # 登陆函数
    # 设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
    cj = http.cookiejar.LWPCookieJar()
    cookie_support = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)

    url = 'http://acm.hit.edu.cn/hoj/system/login'  # 登陆的界面

    # 这个最好加上，不然由于内部信息默认显示为机器代理，可能被服务器403 Forbidden拒绝访问
    header = {'User-Agent': 'Magic Browser'}

    # 构造Post数据，从抓大的包里分析得出的或者通过查看网页源代码可以得到
    data = {
        'user': 'pipi',  # 你的用户名
        'password': '**********',  # 你的密码，密码可能是明文传输也可能是密文，如果是密文需要调用相应的加密算法加密
        'submit': 'Login'  # 特有数据，不同网站可能不同
    }

    data = urllib.parse.urlencode(data).encode('utf-8')

    # 发送请求，得到服务器给我们的响应
    response = urllib.request.Request(url, data, header)
    # 通过urllib提供的request方法来向指定Url发送我们构造的数据，并完成登录过程
    urllib.request.urlopen(response)

    return


login()
i = 1
url = 'http://acm.hit.edu.cn/hoj/problem/solution/?problem=1'
response = urllib.request.urlopen(url)
html = response.read().decode()
print(html)
