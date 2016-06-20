#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'pi'
__mtime__ = '8/27/2015-027'
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
import subprocess
import sqlite3
import win32crypt

import requests

SOUR_COOKIE_FILENAME = r'C:\Users\pi\AppData\Local\Google\Chrome\User Data\Default\Cookies'
DIST_COOKIE_FILENAME = '.\python-chrome-cookies'


def get_chrome_cookies(url):
    subprocess.call(['copy', SOUR_COOKIE_FILENAME, DIST_COOKIE_FILENAME], shell=True)
    conn = sqlite3.connect(".\python-chrome-cookies")
    ret_dict = {}
    for row in conn.execute("SELECT host_key, name, path, value, encrypted_value FROM cookies"):
        # if row[0] not in url:
        if row[0] != url:
            continue
        print(row[0])
        ret = win32crypt.CryptUnprotectData(row[4], None, None, None, 0)
        ret_dict[row[1]] = ret[1].decode()
    conn.close()
    subprocess.call(['del', '.\python-chrome-cookies'], shell=True)
    return ret_dict


DOMAIN_NAME = '.jobbole.com'
get_url = r'http://www.jobbole.com/'
response = requests.get(get_url, cookies=get_chrome_cookies(DOMAIN_NAME))
print(response.text)
