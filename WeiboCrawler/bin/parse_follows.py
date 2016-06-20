#coding=utf-8
import sys
from html.parser import HTMLParser 
class UserInfo:
	def __init__(self):
		self.uid = '-'
		self.fnick = '-'
		self.sex = '-'
		self.num_follow = '-'
		self.num_fans = '-'
		self.num_weibo = '-'
		self.address = '-'
		self.follow_client = '-'
		self.intro = '-'
	def __str__(self):
		return '\t'.join([self.uid,self.fnick,self.sex,self.num_follow,self.num_fans,self.num_weibo,self.address,self.follow_client,self.intro])
class FollowsParse(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)  
        	self.span = False
		self.a = False
		self.flags = {'微博':False,'粉丝':False,'关注':False}
		self.info = None
		self.address = False
		self.address1 = False
		self.new_user = False
		self.client = False
		self.intro = False
		self.follows = []
	def handle_starttag(self,tag,attrs):  
		if tag == 'li' and ('class', r'\"follow_item') in attrs:		
			for attr in attrs:
				#后边滤掉话题微博
				if attr[0] == 'action-data' and ('sex=f' in attr[1] or 'sex=m' in attr[1]):
					text = attr[1][2:-2]
					items = text.split('&')
					self.info = UserInfo()
					if len(items) == 3:
						self.info.uid = items[0][4:]
						self.info.fnick = items[1][6:]
						self.info.sex = items[2][4:]
						self.new_user = True
					

		if self.new_user == False:
			return
		if tag == 'span':
			self.span = True
		if tag == 'a':
			self.a = True
		if tag == 'a' and  ('class', '\\"from\\"') in attrs:
			self.client = True
		if tag == 'em' and ('class', '\\"tit') in attrs:
			self.address = True
		if tag == 'div' and ('class', '\\"info_intro\\"') in attrs:
			self.intro = True
		
	def handle_data(self,data):
		data = data.strip()
		if self.new_user == False:
			return
		
		if self.span:
			key = data.strip()
			if key in self.flags:
				self.flags[key] = True
			if self.address and self.address1:
				self.address = False
				self.address1 = False
				self.info.address = data.strip()
			if self.intro:
				self.info.intro = data
				self.intro = False
			self.span = False
		if self.address and data.strip() == '地址':
			self.address1 = True
		if self.a:
			self.a = False
			if self.flags['粉丝']:
				self.info.num_fans = data.strip()
			if self.flags['微博']:
				self.info.num_weibo = data.strip()
			if self.flags['关注']:
				self.info.num_follow = data.strip()
			for key in self.flags:
				self.flags[key] = False
		



		if self.client:
			self.info.follow_client = data.strip()
			self.client = False
			self.new_user = False
			self.follows.append(self.info)

def parse_follows(html):
	pos1 = html.find(r'<ul class=\"follow_list\"')
	pos2 = html.find(r'\r\n<\/div>\r\n\t<div class=\"WB_cardpage')
	follow_list = html[pos1:pos2]
	parse = FollowsParse()
	parse.feed(follow_list)
	parse.close()
	return parse.follows
	'''
	ret = []
	for follow in parse.follows:
		ret.append(follow.uid)
	return ret
	'''
if __name__ == '__main__':
	html = sys.stdin.read()
	follows = parse_follows(html)
	for info in follows:
		print(info.uid)
