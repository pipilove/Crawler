from collections import OrderedDict
from pprint import pprint
import re

s = '''GET / HTTP/1.1
Host: www.jobbole.com
Connection: keep-alive
Cache-Control: max-age=0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36
Accept-Encoding: gzip, deflate, sdch
Accept-Language: zh-CN,zh;q=0.8,en;q=0.6
Cookie: wordpress_logged_in_0efdf49af511fd88681529ef8c2e5fbf=pipiyn%7C1440999016%7C639ce0a07443e9fea13e1dc6c49dd9c1'''
slist = s.split('\n')
reguale_slist = [re.split(':*\s*', item, maxsplit=1) for item in slist]
# print(OrderedDict(reguale_slist))
stmp = [str(item) for item in OrderedDict(reguale_slist).items()]
# print(stmp)
stt = [item.strip('()').replace(',', ':', 1)  for item in stmp]
print('{', ', '.join(stt), '}')