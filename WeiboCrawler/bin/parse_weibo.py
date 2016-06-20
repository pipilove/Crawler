#coding=utf-8
import sys
from bs4 import BeautifulSoup
import re
import time

comment_re = re.compile(r'>评论\s(\d+)')
comment_num_re = re.compile(r'>评论\s*(\d*)')
retweet_re = re.compile(r'>转发\s(\d+)')
favor_re = re.compile(r'title=\\"赞\\".+<em>(\d+)<\\/em>')
#content_re = re.compile(r'feed_list_content[^>]+>\\n([^(?:<\\/div>)]+)')
#content_re = re.compile(r'feed_list_content[^>]+>\\n([^(?:\\n)]+)')
content_re = re.compile(r'feed_list_content[^>]+>\\n(.+)<div class=\\"WB_from S_txt2\\">\\n')
del_pic_re = re.compile(r'fl_pic_list')
time_re = re.compile(r'date=\\"(\d{10})000\\"')
	


#z这里只抓取发的微博，对于转发的不抓取
def get_weibo(item):
	comments = comment_re.findall(item)
	retweets = retweet_re.findall(item)
	favors = favor_re.findall(item)
	comment_num = comment_num_re.findall(item)
	if len(comment_num) > 1:
		return
	if len(comments) > 1 :
		#转发微博
		return
	elif len(comments) == 0 or len(retweets) == 0 or len(favors) ==0:
		#异常微博
	#	return
		pass
	else:
		comment = comments[0]
	content = content_re.findall(item)
	if len(content) >0:
		content = content[0]
	if len(content) ==0:
		#微博异常
		return
	
	time_str = time_re.findall(item)
	if len(time_str) >0:
		time_str = time_str[0]
		date = time.localtime(float(time_str))
		time_str = time.strftime("%Y-%m-%d %H:%M:%S",date)	
	else:
		time_str = '-'
	#下边函数可以整理为一个
	if r'class=\"W_icon icon_warnS' in content:
		return #已删除微博
	if 'fl_pic_list' in content:
		pos1 = content.find(r'<div node-type=\"fl_pic_list\"')
		pos2 = content.find(r'<\/div>\n',pos1)
		content = content[:pos1]		
	#下边处理成功可以不要上边的
	if 'WB_media_wrap' in content:
		pos3 = content.find(r'<div class=\"WB_media_wrap')
		content = content[:pos3]
	#删除注释
	if '<!--' in content:
		pos4 = content.find(r'<!--')
		content = content[:pos4]
		content = content.strip()

	if "<div node-type='feed_list_media_prev'>" in content:
		pos5 = content.find("<div node-type='feed_list_media_prev'>")
		content = content[:pos5]
		content = content.strip()
	if content.endswith(r'<\/div>\n'):
		pos6 = content.find(r'<\/div>\n')
		content = content[:pos6]
		content = content.strip()
	content = content.replace('\\/','/')
	i = 0
	while r'<a target=\"_blank\"' in content:
		pos7 = content.find(r'<a target=\"_blank\"')
		pos_type = content.find(r'type=',pos7)
		target_type = content[pos_type+5:pos_type+10]
		if target_type == 'topic':
			pos8 = content.find(r'>#',pos7)
			pos8_ = content.find('#</a>',pos8)
			content = content[:pos7] + content[pos8+1:pos8_] +'#'+content[pos8_+5:]
			
		elif target_type == 'atnam':
			pos8 = content.find(r'>@',pos7)
			pos8_ = content.find('</a>',pos8)
			content = content[:pos7] + content[pos8+1:pos8_] + content[pos8_+4:]
		i += 1
		if i > 10:
			break
	#替换@连接为 @人名@

	i = 0
	while r"<a target='_blank'" in content:
		pos7 = content.find(r"<a target='_blank'")
		pos8 = content.find(r'</a>',pos7)
		content = content[:pos7] + '[连接或表情]'+ content[pos8+4:]
		i += 1
		if i > 10:
			break
	#去除连接
	i = 0
	while r'<a class=\"W_btn_b btn_22' in content:
		pos9 = content.find(r'<a class=')
		pos10 = content.find('</a>',pos9)
		content = content[:pos9] +'{网页连接}'+ content[pos10+4:]
		i += 1
		if i > 6:
			break
	i = 0
	#去除表情连接
	while r'<img render=' in content:
		pos11 = content.find(r'<img render=')
		pos12 = content.find('/>',pos11)
		title_re = re.compile(r'title=\\"\[(.{0,10})\]')
		title = title_re.findall(content)
		if len(title) == 0:
			title ="[未知表情或图片]"
		else:
			title = title[0]
		content = content[:pos11] + '['+title +']' + content[pos12+2:]
		i += 1
		if i > 20:
			break
	i = 0
	#统一去除a标签
	while '<a' in content:
		pos1 = content.find('<a')
		pos2 = content.find('</a>',pos1)
		if len(content) >pos2+4:
			content = content[:pos1] + content[pos2+4:]
		else:
			content = content[:pos1]
		
		i += 1
		if i > 10:
			break
	i =0
	while r'<a ignore=\"ignore\"' in content:
		pos21 = content.find(r'<a ignore=\"ignore\"')
		pos22 = content.find(r'</a>\n',pos21)
		if len(content) >pos22 + 4:
			content = content[:pos21] + content[pos22+4:]
		else:
			content = content[:pos21]
		
		i += 1
		if i > 10:
			break
	i =0
	while r'<img ' in content:
		pos21 = content.find(r'<img')
		pos22 = content.find(r'>',pos21)
		if len(content) > pos21+1:
			content = content[:pos21] + content[pos22+1:]
		else:
			content = content[:pos21]
			
		i += 1
		if i > 10:
			break
	if r'<span class=\"W_icon_feedhot\">' in content:
		pos23 = content.find(r'<span class=\"W_icon_feedhot\">')
		pos24 = content.find(r'</span>\n',pos23)
		if pos24+10 < len(content):
			content = content[:pos23] + content[pos24+10:].strip()
		else:
			content = content[:pos23].strip()

	while content.startswith(r'\n'):
		content = content[2:]
	content = content.strip()
	#if "平凡的世界" not in content:
	#	return 
	if content.endswith(r'</div>\n'):
		content = content[:-8].strip()
	if content.endswith(r'\n'):
		content = content[:-2].strip()
	if len(comments) == 0:
		comments.append('0')	
	if len(retweets) == 0:
		retweets.append('0')	
	if len(favors) == 0:
		favors.append('0')	
	return '\t'.join([time_str,retweets[0],comments[0],favors[0],content])







#提取微博正文的方法
#1.按div的class属性分割
#@author liushaojiang
#@date 20150314

def get_all(text):
	infos = text.split('\n')
	weibo_contents = []
	for line in infos:
		if 'feed_list_repeat' in line:
			#提取出微博正文
			items = line.split('feed_list_repeat')	
			#删除正在加载
			items.pop(-1)
			for item in items:
				out = get_weibo(item)
				if out:
					weibo_contents.append(out)
	return weibo_contents

if __name__ == '__main__':
	text = sys.stdin.read()
	contents = get_all('123',text)
	for item in contents:
		print(item)
