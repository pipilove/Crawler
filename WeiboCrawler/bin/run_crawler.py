#!/usr/bin/python
# coding=utf-8
import datetime
import os
import re
import sys
import login
import parse_weibo
import time
import parse_follows
import set_seeds

from socket import error as SocketError

from parse_follows import UserInfo

base_path = ''
base = ''
# 主页我的id
myid_re = re.compile(r"\$CONFIG\['uid'\]\s*=\s*'(\w+)';")
# 他人页的他人id
userid_re = re.compile(r"\$CONFIG\['oid'\]\s*=\s*'(\w+)';")
user_nickname_re = re.compile(r"\$CONFIG\['onick'\]\s*=\s*'(.+)';")



# 他关注的人的id
followid_re = re.compile(r"uid=(\w+)\&fnick=(.{1,24})\&sex=(.)")
# 我的关注
myfollowid_re = re.compile(r"nick=(.{1,24})\&uid=(\w+)\&sex=(.)")
# 关注人数
# home_num_re = re.compile(r'<strong class=\\"W_f18\\">(\d+)<\\/strong><span class=\\"S_txt2\\">(.{2})<\\/span>')
home_num_re = re.compile(r'<strong class=\\"W_f1\d\\">(\d+)<\\/strong><span class=\\"S_txt2\\">(.{6})')
location_re = re.compile(
    r'<span class=\\"item_text W_fl\\">\\r\\n(?:\s+(?:\\t){5,7})+(.{0,15})(?:\\t)+\s+(?:\\t)+<\\/span>')
intro_re = re.compile(r'<div class=\\"pf_intro\\" title=\\"(.{1,100})\\">')
accounts = []
opener = None
seen = set()
queue = set()
users = {}
weibo = 'http://weibo.com/'

time_f = open('%sdir_names' % base_path, 'a')
time_str = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
time_f.write('%s\n' % time_str)
time_f.close()
flag_continue = False
if not os.path.exists(base_path + '../data'):
    os.system('mkdir %s' % (base_path + '../data'))
weibo_html = '%sweibo_html' % (base_path + '../data/')
if not os.path.exists(weibo_html):
    os.system('mkdir %s' % weibo_html)
time_path = base_path + '../data'


def open_file():
    global weibo_f
    global log_f
    global user_f
    global queue_f
    global seen_f
    global relation_f
    user_f = open('%s/users' % time_path, 'w')
    relation_f = open('%s/relation' % time_path, 'w')
    weibo_f = open('%s/weibos' % time_path, 'w')
    log_f = open('%s/log' % time_path, 'w')
    queue_f = open('%s/queue' % time_path, 'w')
    seen_f = open('%s/seen' % time_path, 'w')


def open_file_append():
    global weibo_f
    global log_f
    global user_f
    global queue_f
    global seen_f
    global relation_f
    user_f = open('%s/users' % time_path, 'a')
    relation_f = open('%s/relation' % time_path, 'a')
    weibo_f = open('%s/weibos' % time_path, 'a')
    log_f = open('%s/log' % time_path, 'a')
    queue_f = open('%s/queue' % time_path, 'a')
    seen_f = open('%s/seen' % time_path, 'a')


def log(text):
    now = datetime.datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    log_f.write('%s %s\n' % (now, text))
    log_f.flush()


if len(sys.argv) == 2 and sys.argv[1] == 'continue':
    flag_continue = True
    open_file_append()
    log('接着上次爬取继续运行')
else:
    flag_continue = False
    open_file()
    log('重新初始化爬虫')


def close_file():
    global weibo_f
    global log_f
    global user_f
    global queue_f
    global seen_f
    global relation_f
    weibo_f.close()
    log_f.close()
    user_f.close()
    queue_f.close()
    seen_f.close()
    relation_f.close()


def update_account(info):
    global opener
    i = 0
    while len(accounts) > 0:
        i = i + 1
        (username, password) = accounts.pop()
        log('account error info:%s\n' % info)
        log('account updated-->username=%s#password=%s  第%s次pop账号' % (username, password, i))
        # 账号异常应该在login.get_opener()函数中得到验证，若等你失败则返回None
        opener = login.get_opener(username, password)
        if opener != None:
            return True
        else:
            log('accounts locked-->username=%s\tpassword=%s' % (username, password))
    if len(accounts) == 0:
        return False


def url2html(url):
    try:
        html = opener.open(url).read()
        check_html(html, 'follow')
        return html
    except:
        log('catch except')
        update_account('catch net except')
    return None


def check_html(html, page):
    error1 = r'<div class="note"><span class="W_icon icon_rederrorB"></span><em class="S_link1">抱歉，您的帐号存在异常，目前无法进行登录。</br><a href="http://help.weibo.com/faq/q/85/12557#12557">查看帮助</a></em></div>'
    error2 = r'<title>微博帐号解冻 新浪微博-随时随地分享身边的新鲜事儿</title>'
    error3 = r'<p>你所在的帐号、IP或应用由于违反了新浪微博的安全检测规则，暂时无法完成此操作，正确输入验证码答案即可正常访问。如有疑问，请点击<a'
    if error1 in html:
        flag = update_account('抱歉，您的帐号存在异常，目前无法进行登录');
        if flag == False:
            log('list of accounts is empty!')
            sys.exit('账号空了')
    if error2 in html:
        flag = update_account('微博帐号解冻');
        if flag == False:
            log('list of accounts is empty!')
            sys.exit('账号空了')
    if error3 in html:
        flag = update_account('ip?');
        if flag == False:
            log('list of accounts is empty!')
            sys.exit('账号空了')
    '''

    if r'<div class=\"WB_from S_txt2\">' not in html and page == 'home':
        flag = update_account('全图屏蔽');
        if flag == False:
            log('list of accounts is empty!')
            sys.exit('账号空了')

    if r'\r\n<\/div>\r\n\t<div class=\"WB_cardpage' not in html and page == 'follow':
        flag = update_account('全图屏蔽');
        if flag == False:
            log('list of accounts is empty!')
            sys.exit('账号空了')
    '''


def his_follow(user_id):
    base_url = weibo + user_id + '/follow'
    all_follows = []
    for i in range(1, 5):
        url = base_url + '?page=' + str(i)
        html = url2html(url)
        if html == None:
            log('erro url=%s html=None' % url)
            continue
        try:
            follows = parse_follows.parse_follows(html)
        except:
            continue
        all_follows.extend(follows)
    return all_follows


def crawl(uid):
    # 用户关系
    follows = his_follow(uid)
    for info in follows:
        user_id = info.uid
        if (user_id not in seen) and (user_id not in queue):
            # 待爬取列表
            queue.add(user_id)
            queue_f.write(user_id + '\n')
            queue_f.flush()

    follow_ids = []
    for user in follows:
        user_f.write(uid + '\t' + str(user) + '\n')
        user_f.flush()
        follow_ids.append(user.uid)

    relation = ''
    if len(follows) > 0:
        relation = '_'.join(follow_ids)
    relation_f.write(uid + '\t' + relation + '\n')

    # 用户微博内容
    url = weibo + 'u/' + uid
    html = url2html(url)
    if html == None:
        log('erro url=%s html=None' % url)
        return
    html_f = open('%s/%s' % (weibo_html, uid), 'w')
    html_f.write(html)
    html_f.close()
    weibos = parse_weibo.get_all(html)
    for item in weibos:
        weibo_f.write(uid + '\t' + item + '\n')
        weibo_f.flush()

    # 已爬取列表
    seen.add(uid)
    seen_f.write(uid + '\n')
    seen_f.flush()


def init():
    global queue
    global seen
    queue, seen = set_seeds.set_seeds(flag_continue)
    log('seeds info:len(queue)=%s,len(seen)=%s' % (len(queue), len(seen)))
    accounts_f = open('%saccounts' % base_path)
    for line in accounts_f:
        line = line.strip()
        if line == '':
            continue
        items = line.split('----')
        username = items[0].strip()
        password = items[1].strip()
        accounts.append((username, password))
    accounts_f.close()


def main():
    init()

    flag = update_account('初始化账号')
    if flag == False:
        log('list of accounts is empty!')
        sys.exit('账号空了')

    num = 0
    # 将初始化的queue添加到文件中
    # 若自定义种子，才有此操作
    if not flag_continue:
        for q in queue:
            queue_f.write(str(q) + '\n')
            queue_f.flush()
    while len(queue) > 0 and len(seen) < 10000000:
        uid = queue.pop()
        crawl(uid)
        num += 1
        if num % 100 == 0:
            log('len(queue)=%s,len(seen)=%s' % (len(queue), len(seen)))

    log('end')
    close_file()


def reset_list():
    running_queue = open('../data/running_queue', 'w')
    running_seen = open('../data/running_seen', 'w')
    for uid in ruuning_seen:
        uid = uid.strip()
        seen.add(uid)
    running_seen.close()
    for uid in queue:
        uid = uid.strip()
        queue.append(uid)
    running_queue.close()


def save_list():
    running_queue = open('../data/running_queue', 'w')
    running_seen = open('../data/running_seen', 'w')
    for uid in seen:
        running_seen.write(uid + '\t')
    running_seen.close()
    for uid in queue:
        running_queue.write(uid + '\t')
    running_queue.close()


def update_state():
    path = '%spid' % base_path
    state = 'start'
    f = open(path, 'w')
    timestamp = int(time.time())
    timestamp = str(timestamp)
    f.write("timestamp:%s\n" % timestamp)
    f.write("pid:%s\n" % os.getpid())
    f.write('state:%s:%s\n' % (state, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
    f.close()


if __name__ == '__main__':
    update_state()
    main()
    close_file()
    path_str = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    if not os.path.exists('%slogs' % base_path):
        os.system('mkdir %slogs' % base_path)
    os.system('mv pid %slogs/pid_%s' % (base_path, path_str))
    sys.exit('爬取结束，已爬取列表')
