# coding=utf-8
"""boL<span style="font-family:SimSun;">ogin.py</span>"""
"""运行登陆成功后，同目录下会有一个gauidepage.html"""
"""version 1.0"""
"""2014/8/7"""
"""fancy"""

import urllib.request
import urllib.error
import urllib.parse
import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
import json
import binascii
import time

import re
import base64
import rsa


def Initiliaze():
    # initial url
    global prelogin_url, login_url, redir_url
    prelogin_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack" \
                   "&su=&rsakt=mod&client=ssologin.js(v1.4.18)"
    login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    redir_url = 'http://weibo.com/guide/welcome'

    # Initialize the opener
    global opener
    cj = http.cookiejar.LWPCookieJar()
    cookie_support = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)

    # initilaze header
    global headers
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
               'Referer': 'http://weibo.com/'}


def Prelogin(url):
    global opener
    data = opener.open(url).read().decode()
    try:
        json_data = re.search('\((.*?)\)', data).group(1)
        data = json.loads(json_data)
        # print("***Prelogin data******************************:\n", data)

        servertime = str(data['servertime'])
        nonce = data['nonce']
        pubkey = data['pubkey']
        rsakv = data['rsakv']

        return servertime, nonce, pubkey, rsakv
    except:
        print("get Prelogin data error")
        return None


def GetUser(username):
    username_ = urllib.parse.quote(username).encode()
    username = base64.encodebytes(username_)[:-1]
    # print("***encrypt username******************************:\n",username)
    return username


def GetPwd(pwd, servertime, nonce, pubkey, rsakv):
    pubkey_ = int(pubkey, 16)
    key = rsa.PublicKey(pubkey_, 65537)  # 创建公匙
    message = (str(servertime) + '\t' + str(nonce) + '\n' + str(pwd)).encode()  # 拼接明文js加密文件中得到
    pwd_ = rsa.encrypt(message, key)  # 加密
    pwd_ = binascii.b2a_hex(pwd_)  # 将加密信息转换为16进制

    # print "***encrypt password******************************:\n",pwd_
    return pwd_


# construct postdata
def GetPostData(username, password, servertime, nonce, rsakv):
    postdata = {'pwencode': 'rsa2',
                'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController'
                       '.feedBackUrlCallBack'}
    # postdata = {'encoding': 'UTF-8', 'entry': 'weibo', 'from': '', 'gateway': '1', 'nonce': 'F1QRA7',
    #         'pagerefer': 'http://passport.weibo.com/visitor/visitor?a=enter&url=http://weibo.com/&_rand'
    #                      '=1407411069.5054', 'prelt': '56', 'pwencode': 'rsa2', 'returntype': 'META', 'rsakv': '',
    #         'savestate': '7', 'servertime': '', 'service': 'miniblog', 'sp': '', 'sr': '1366*768', 'su': '',
    #         'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController'
    #                '.feedBackUrlCallBack', 'useticket': '1', 'vsnf': '1'}
    postdata['nonce'] = nonce
    postdata['rsakv'] = rsakv
    postdata['servertime'] = servertime
    postdata['sp'] = password
    postdata['su'] = username
    return urllib.parse.urlencode(postdata).encode()


def get_opener(username, password):
    Initiliaze()
    # prelogin
    servertime, nonce, pubkey, rsakv = Prelogin(prelogin_url)

    # encrypt
    username = GetUser(username)
    password = GetPwd(password, servertime, nonce, pubkey, rsakv)

    # ready postdata
    postdata = GetPostData(username, password, servertime, nonce, rsakv)
    # print(postdata)

    # login
    req = urllib.request.Request(login_url, data=postdata, headers=headers)
    data = opener.open(req).read().decode('gb2312')
    # print(data)
    # get new url并访问新url，获取和保存登陆使用的cookie
    newlogin_url = re.findall("location.replace\(\'(.*?)\'\);", data)
    # 验证登陆是否成功


    if len(newlogin_url) == 0:
        return None
    # return (None,'Error' + str(openerid))
    newlogin_url = newlogin_url[0]
    # print(newlogin_url)
    try:
        opener.open(newlogin_url)
    except:
        time.sleep(100)
        return None
    # 通过cookie直接访问guide页面
    try:
        guidepage = opener.open(redir_url).read().decode('gb2312')
    except:
        guidepage = opener.open(redir_url).read().decode()
    print(guidepage)

    if '<title>微博帐号解冻 新浪微博-随时随地分享身边的新鲜事儿</title>' or r'<div class="note"><span class="W_icon ' \
                                                     r'icon_rederrorB"></span><em ' \
                                                     r'class="S_link1">抱歉，您的帐号存在异常，目前无法进行登录。</br>' in guidepage:
        return None
    return opener


if __name__ == '__main__':
    opener = get_opener('xingshang1992@163.com', '*************')
    # opener = get_opener('zpdr917529075@163.com', 'uuu888')
    if opener != None:
        print('login success')
    else:
        print('erro')
    '''
    for line in open('password.ini'):

        line = line.strip().split('#')
        opener = get_opener(line[0],line[1])
        if opener != None:
            #print 'login success'
            print '----'.join(line)
        else:
            pass
            #print 'login error'
jifei7062594@163.com#qqq555
lunlun9131354@163.com#qq555
panwoyan404826@163.com#qqq555
kepopanganjia@163.com#qqq555
yun24302571@163.com#qqq555
chejiu735933@163.com#qqq555
daodong800@163.com#qqq555
ciyong748155@163.com#qqq555
yannai446@163.com#qqq555
meidu3733737@163.com#qqq555
'''
