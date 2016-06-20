# coding=utf-8
import os
import sys
import time

base = '/usr/local/tomcat/webapps/ROOT/weibo/py/bin/'
path = '%spid' % base


def readpid():
    dic = {}
    f = open(path)
    for line in f:
        line = line.strip().split(':')
        dic[line[0]] = line[1]
    f.close()
    return dic


def update_state(state):
    f = open(path, 'a')
    f.write('state:%s:%s\n' % (state, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
    f.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: python pid.py start|restart|stop|kill|state')
        sys.exit('输入错误')
    signal = sys.argv[1]
    if not os.path.exists(path):
        if signal == 'start':
            os.system('python %srun_crawler.py' % base)
        elif signal == 'state':
            sys.exit('not_run')
        else:
            sys.exit('程序未启动，请使用 python *.py start')


    elif os.path.exists(path):
        dic = readpid()
        pid = dic['pid']
        timestamp = dic['timestamp']
        state = dic['state']
        if signal == 'start':
            sys.exit('已经启动，无需重启')
        elif signal == 'restart':
            if state == 'stop':
                update_state('restart')
                os.system('kill -CONT %s' % pid)
            else:
                sys.exit('指令错误,state=%s' % state)
        elif signal == 'stop':
            if state == 'start' or state == 'restart':
                update_state('stop')
                os.system('kill -STOP %s' % pid)
                sys.exit('程序暂停')
            else:
                sys.exit('指令错误,state=%s' % state)
        elif signal == 'kill':
            path_str = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
            if not os.path.exists('%slogs' % base):
                os.system('mkdir %slogs' % base)
            update_state('kill')
            os.system('mv %spid %slogs/pid_%s' % (base, base, path_str))
            os.system('kill -9 %s' % pid)
            sys.exit('程序停止 killed')
        elif signal == 'state':
            sys.exit(state)
        elif signal == 'timestamp':
            now = int(time.time())
            old = int(timestamp)
            distance = now - old
            hour = distance / 3600
            minute = distance % 3600 / 60
            second = distance % 60
            sys.exit('%s时%s分%s秒' % (hour, minute, second))
        else:
            print('usage: python pid.py restart|stop|kill|state')
