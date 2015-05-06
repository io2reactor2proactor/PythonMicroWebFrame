#-*- coding: utf-8 -*-

from wsgiref.simple_server import make_server
from micro_frame import *
from threading import *
import os, stat, sys
import cookie
import datetime
import random

urls = (
    (r'/', r'index'),
    (r'/hello/(?P<other>.*)', r'hello'),
    (r'/index/(?P<id>\d+)/(?P<num>\d+)', r'test'),
    (r'/(?P<user>[a-zA-Z]+)/(?P<id>\d+)/(?P<num>\d+)', r'user'),
    (r'/index/(?P<id>\d+)', r'new_test'),
    (r'/(blog|topic)/(\w+)', r'blog'),
    (r'/favicon.ico', r'icon'),
    (r'/login', r'login'),
)

class index:
    def GET(self):
		set_header()

		print('\n\n')
		for index in ctx.response.response_headers:
			print index
		print('\n\n')

		return '''
		<form action="/login" method="post" enctype ="multipart/form-data" target="_blank">
		<p>UserName <input name="username" type="text"></p>
		<p>PassWord <input name="password" type="password"></p>
		<p>TextFile <input name="file_one" type="file"></p>
		<p>TextFile <input name="file_two" type="file"></p>
		<p>Math <input name="math" type="checkbox" value='on'></p>
		<p>English <input name="english" type="checkbox" value='on'></p>
		<p>Chinese <input name="subject" type="radio" value="chinses"></p>
		<p>Physics <input name="subject" type="radio" value="physics"></p>
		<p>Me_Text <textarea rows="10" cols="30" name="mytext"></textarea></p>
		<p>Mobiles
		<select name="mobiles">
			<option value="apple">Apple</option>
			<option value="vivo">Vivo</option>
			<option value="huawei">HuaWei</option>
			<option value="xiaomi">XiaoMi</option>
		</select>
		</p>
		<p><button type="submit">Sign In</button>
		<button type="reset">Reset</button></p>
		</form>'''
	
    def _write_file(self, file_name, file_content):
		with open(r'test\\' + file_name, 'ab+') as file:
			file.write(file_content)
		print 'save file ok.....'

    def POST(self):
		# ctx.response.response_headers
		for k, v in ctx.request.form_data.iteritems():
			print type(v), v
			if k == 'file_one':
				# file_name = 'save_one.txt'
				self._write_file(v[2], v[0])
				print type(v[1])
			elif k == 'file_two':
				# file_name = 'save_two.txt'
				self._write_file(v[2], v[0])
				print type(v[1])
			else:
				yield '<p>%s -> %s</p>' % (k, v[0])
		# return 'post ok'

class hello:
	def GET(self, *tt, **dd):
		set_header()

		print('\n\n')
		for index in ctx.response.response_headers:
			print index
		print('\n\n')

		return "hello : %s" % tt[0]

class test:
	def GET(self, *tt, **dd):
		set_header()
		print 'tuple length : ', len(tt)
		print 'dict length : ', dd
		return 'test %s-%s' % (tt[0], tt[1])

class new_test:
	def GET(self, *tt, **dd):
		set_header()
		print 'tuple length : ', len(tt)
		print 'dict length : ', dd
		return 'new_test %s' % tt[0]

class user:
	def GET(self, *tt, **dd):
		set_header()
		print 'tuple length : ', len(tt)
		print 'dict length : ', dd
		return "user (%s-%s-%s)" % (tt[0], tt[1], tt[2])

class blog:
	def GET(self, *tt):
		set_header()
		return "blog or topic [%s-%s]" % (tt[0], tt[1])

class icon:
	def GET(self, *tt):
		set_header()
		return "icon ok"

class login:
	def GET(self):
		set_header()
		return "login ok"

	def get_io_data(self, like_file):
		print 'run into function'
		# print 'next() : ', like_file.next()
		buff = ''
		while True:
			print 'run into loop'
			buff = like_file.read(1024)
			print 'buff length : ', len(buff)
			if not len(buff):
				break
			# print 'file content : ', buff

	def _write_file(self, file_name, file_content):
		with open(r'test\\' + file_name, 'ab+') as file:
			file.write(file_content)
		print 'save file ok.....'

	def io_file(self, file_name, like_file):
		sum = 0
		buff = ''
		print 'outside buffer length : ', len(buff)
		with open(r'test\\' + file_name, 'ab+') as file:
			print 'run into file inside'
			while True:
				print 'run into loop'
				buff = like_file.read(8192)
				if not len(buff):
					break
				sum = sum + len(buff)
				# print len(buff), ',', type(buff)
				print 'current total length :', sum
				file.write(buff)
		print 'save file ok.....'

	def POST(self):
		for k, v in ctx.request.form_data.iteritems():
			# print type(v), v
			if k == 'file_one':
				# file_name = '1.txt'
				# self._write_file(file_name, v[0])
				# self._write_file(v[2], v[0])
				print 'file_one type : ', type(v[1])
				print 'file_one : ', dir(v[1])
				# print 'file_one next : ', help(v[1].next)
				# print 'read result is : ', self.get_io_data(v[1])
				self.io_file(v[2], v[1])
			elif k == 'file_two':
				# file_name = '2.txt'
				# self._write_file(file_name, v[0])
				# self._write_file(v[2], v[0])
				print 'file_two type : ', type(v[1])
				print 'file_two : ', dir(v[1])
				# print 'file_two next : ', help(v[1].next)
				# print 'read result is : ', self.get_io_data(v[1])
				self.io_file(v[2], v[1])
			else:
				# yield '<p>%s -> %s</p>' % (k, v)
				yield '''<p><img alt="Alt text" src="http://www.oschina.net/img/ostools.gif" title="Optional title" /></p>'''

def make_cookie():
	expires = datetime.datetime.now() + datetime.timedelta(days=30)
	test = cookie.SimpleCookie()
	# test["id"] = random.randint(0,1000000000)
	test["id"] = 'qwert'
	# test["id"]["domain"] = "127.0.0.1"
	# test["id"]["path"] = "/"
	test["id"]["max-age"] = 0
	# test["id"]["expires"] = expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT")
	return test["id"].output()[12:]

def set_header():
	print(make_cookie())
	ctx.response.add_header('Content-Type', 'text/html; charset=utf-8')
	ctx.response.add_header('X-Powered-By', 'test/0.1')
	ctx.response.add_header('Vary', 'Accept-Encoding')
	ctx.response.add_header('Cache-Control', 'max-age=60')
	ctx.response.add_header('X-UA-Compatible', 'IE=Edge,chrome=1')
	# ctx.response.add_header('Set-Cookie', 'uc123=123; path=/')
	# ctx.response.add_header('Set-Cookie', 'dwl=456; path=/')
	ctx.response.add_header('Set-Cookie', make_cookie())

# name = r'hello'
# print type(globals())
# for k, v in globals().items():
	# print k, v
# print '------------------------------'
# print globals().get(name), type(globals().get(name))
# print '------------------------------'
# print dir(globals().get(name))
# print '------------------------------'
# if hasattr(globals().get(name), 'GET'):
	# fn = getattr(globals().get(name), 'GET')
	# print fn, type(fn)
# print '------------------------------'
# for k, v in urls:
	# print k, v
# print '------------------------------'

wsgiapp = my_app(urls, globals())
if __name__ == '__main__':
	print("start server.....")
	run(wsgiapp)