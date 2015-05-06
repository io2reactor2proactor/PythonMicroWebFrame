# -*- coding: utf-8 -*-

import re
import os
import sys
import stat
import traceback
import cgi, threading
import urllib
import cookie

try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

ctx = threading.local()

class Request:
	'''
	web request
	'''

	def __init__(self, environ = None):
		# self._env = environ
		self.bind(environ or {})

	def bind(self, environ):
		self._env = environ

	@property
	def environ(self):
		return self._env

	@property
	def is_multiprocess(self):
		return self._env["wsgi.multiprocess"]
	
	@property
	def http_accept_language(self):
		return self._env["HTTP_ACCEPT_LANGUAGE"]
	
	@property
	def server_protocol(self):
		return self._env["SERVER_PROTOCOL"]
	
	@property
	def server_software(self):
		return self._env["SERVER_SOFTWARE"]
		
	@property
	def request_method(self):
		return self._env["REQUEST_METHOD"]
		
	@property
	def query_string(self):
		return self._env["QUERY_STRING"]
		
	@property
	def wsgi_error(self):
		return self._env["wsgi.errors"]
		
	@property
	def content_length(self):
		return self._env["CONTENT_LENGTH"]
		
	@property
	def http_accept_charset(self):
		return self._env["HTTP_ACCEPT_CHARSET"]
		
	@property
	def http_cache_control(self):
		return self._env["HTTP_CACHE_CONTROL"]
		
	@property
	def http_connection(self):
		return self._env["HTTP_CONNECTION"]
		
	@property
	def remote_addr(self):
		return self._env["REMOTE_ADDR"]
		
	@property
	def server_port(self):
		return self._env["SERVER_PORT"]
		
	@property
	def http_accept(self):
		return self._env["HTTP_ACCEPT"]
	
	@property
	def url_scheme(self):
		return self._env["wsgi.url_scheme"]
		
	@property
	def wsgi_input(self):
		return self._env["wsgi.input"]
		
	@property
	def http_host(self):
		return self._env["HTTP_HOST"]
		
	@property
	def is_multithread(self):
		return self._env["wsgi.multithread"]
		
	@property
	def path_info(self):
		return self._env["PATH_INFO"]
		
	@property
	def file_wrapper(self):
		return self._env["wsgi.file_wrapper"]
		
	@property
	def http_accept_encoding(self):
		return self._env["HTTP_ACCEPT_ENCODING"]
		
	@property
	def version(self):
		return self._env["wsgi.version"]
		
	@property
	def run_once(self):
		return self._env["wsgi.run_once"]
		
	@property
	def gateway_interface(self):
		return self._env["GATEWAY_INTERFACE"]
		
	@property
	def http_user_agent(self):
		return self._env["HTTP_USER_AGENT"]
		
	@property
	def number_of_processors(self):
		return self._env["NUMBER_OF_PROCESSORS"]
		
	@property
	def content_type(self):
		return self._env["CONTENT_TYPE"]
		
	@property
	def form_data(self):
		form = {}
		fs = cgi.FieldStorage(fp=self._env['wsgi.input'], environ=self._env, keep_blank_values=True)
		# print help(fs)
		# print dir(fs)
		# print 'file type : ', type(fs.file)
		# print 'file : ', fs.file
		# print 'filename type : ', type(fs.filename)
		# print 'filename 1 : ', fs.filename
		# print 'filename 2 : ', fs.name
		# print 'file content : ', type(fs.getlist('myfile')), ',', fs.getlist('myfile')
		# print 'username : ', type(fs.getlist('username')), ',', fs.getlist('username')
		# print 'password : ', type(fs.getlist('password')), ',', fs.getlist('password')
		# print 'all value : '
		# for id in xrange(len(fs.value)):
			# print fs.value[id]
		print 'one value : ', fs.value[0].name, fs.value[0].file, fs.value[0].filename, fs.value[0].value
		# print 'one value : ', fs.value[1].name, fs.value[1].file, fs.value[1].filename, fs.value[1].value
		# print 'one value : ', fs.value[2].name, fs.value[2].file, fs.value[2].filename, fs.value[2].value
		# print 'one value : ', fs.value[3].name, fs.value[3].file, fs.value[3].filename, fs.value[3].value
		# print 'one value : ', fs.value[4].name, fs.value[4].file, fs.value[4].filename, fs.value[4].value
		# print 'one value : ', fs.value[5].name, fs.value[5].file, fs.value[5].filename, fs.value[5].value
		# print 'one value : ', fs.value[6].name, fs.value[6].file, fs.value[6].filename, fs.value[6].value
		# print 'one value : ', fs.value[7].name, fs.value[7].file, fs.value[7].filename, fs.value[7].value
		# print 'one value : ', fs.value[8].name, fs.value[8].file, fs.value[8].filename, fs.value[8].value
		print '----------------------'
		# print 'help value attr 1: ', fs.value[0].name, ',', fs.value[0].filename, ',', fs.value[0].value
		# print 'help value attr 2: ', fs.value[1].name, ',', fs.value[1].filename, ',', fs.value[1].value
		# print 'help value attr 3: ', fs.value[2].name, ',', fs.value[2].filename, ',', fs.value[2].value
		print '----------------------'
		# print 'fp : ', fs.fp.name
		# print 'fp : ', fs.fp.fileno
		# print 'fp type : ', type(fs.fp)
		# print 'dir fp : ', dir(fs.fp)
		# print 'length : ', fs.length
		# print 'innerboundary : ', fs.innerboundary
		# print 'headers : ', fs.headers
		# print 'bufsize : ', fs.bufsize
		# print 'disposition_options : ', fs.disposition_options
		# print 'getlist : ', fs.getlist
		# print 'make_file : ', fs.make_file
		# print 'getfirst : ', fs.getfirst
		# print 'qs_on_post : ', fs.qs_on_post
		# keys = fs.keys()
		# print 'keys :', keys
		# form = dict(zip((key for key in keys), (fs.getvalue(key) for key in keys)))
		# form = dict((key, fs.getvalue(key)) for key in keys)
		form = dict((fs.value[id].name, [fs.value[id].value, fs.value[id].file, fs.value[id].filename]) for id in xrange(len(fs.value)))
		# print 'form : ', form
		# for key in keys:
			# print "------------------"
			# print key, "-->", fs.getvalue(key)
			# print "------------------"
		return form
	
	def environ_specialed_item(self, key):
		return self._env[key]
	
	@property
	def http_cookie(self):
		return self._env.get("HTTP_COOKIE")
		
	def get_cookie_data(self):
		if not hasattr(self, '_cookies'):
			cookies = {}
			cookie_str = self.http_cookie
			print "result : ", cookie_str
			if not cookie_str is None:
				for item in cookie_str.split(';'):
					print item
					delimiter = item.find('=')
					if position > 0:
						cookies[item[:delimiter].strip()] = _unquote(item[delimiter + 1:])
			else:
				self._cookies = {}
			self._cookies = cookies
		return self._cookies
	
	def cookie_specialed_item(self, name, default=None):
		# '''
		# Return specified cookie value as unicode. Default to None if cookie not exists.
		# '''
		return self.get_cookie_data().get(name, default)

class Router:

    def __init__(self, urls=(), fvars={}):
        self._urls = urls
        self._fvars = fvars

    def notfound(self):
		return "not found"

    def dispatch(self):
        return self._delegate()

    def _delegate(self):
        path = ctx.request.path_info
        method = ctx.request.request_method
        print 'request url : ', path
        print 'request method : ', method

        for pattern, name in self._urls:
            regex = r'^' + pattern + r'$'
            match_object = re.match(regex, path)
            if match_object:
                args_tuple_type = match_object.groups()
                args_dict_type = match_object.groupdict()
                # print 'tuple args : ', args
                print 'tuple args : ', args_tuple_type
                # print 'dict args : ', match_object.groupdict()
                print 'dict args : ', args_dict_type
                funcname = method.upper() # function name upper(example: GET or POST)
                classname = self._fvars.get(name) # recording to string find class object
                if hasattr(classname, funcname):
                    func = getattr(classname, funcname)
                    # return func(classname(), *args)
                    return func(classname(), *args_tuple_type, **args_dict_type)
                else:
                    return self.notfound()
        return self.notfound()

RESPONSE_HEADERS = (
    'Accept-Ranges',
    'Age',
    'Allow',
    'Cache-Control',
    'Connection',
    'Content-Encoding',
    'Content-Language',
    'Content-Length',
    'Content-Location',
    'Content-MD5',
    'Content-Disposition',
    'Content-Range',
    'Content-Type',
    'Date',
    'ETag',
    'Expires',
    'Last-Modified',
    'Link',
    'Location',
    'P3P',
    'Pragma',
    'Proxy-Authenticate',
    'Refresh',
    'Retry-After',
    'Server',
    'Set-Cookie',
    'Strict-Transport-Security',
    'Trailer',
    'Transfer-Encoding',
    'Vary',
    'Via',
    'Warning',
    'WWW-Authenticate',
    'X-Frame-Options',
    'X-XSS-Protection',
    'X-Content-Type-Options',
    'X-Forwarded-Proto',
    'X-Powered-By',
    'X-UA-Compatible',
)	

RESPONSE_STATUSES = {
    # Informational
    100: 'Continue',
    101: 'Switching Protocols',
    102: 'Processing',

    # Successful
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    203: 'Non-Authoritative Information',
    204: 'No Content',
    205: 'Reset Content',
    206: 'Partial Content',
    207: 'Multi Status',
    226: 'IM Used',

    # Redirection
    300: 'Multiple Choices',
    301: 'Moved Permanently',
    302: 'Found',
    303: 'See Other',
    304: 'Not Modified',
    305: 'Use Proxy',
    307: 'Temporary Redirect',

    # Client Error
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Acceptable',
    407: 'Proxy Authentication Required',
    408: 'Request Timeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length Required',
    412: 'Precondition Failed',
    413: 'Request Entity Too Large',
    414: 'Request URI Too Long',
    415: 'Unsupported Media Type',
    416: 'Requested Range Not Satisfiable',
    417: 'Expectation Failed',
    418: "I'm a teapot",
    422: 'Unprocessable Entity',
    423: 'Locked',
    424: 'Failed Dependency',
    426: 'Upgrade Required',

    # Server Error
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
    505: 'HTTP Version Not Supported',
    507: 'Insufficient Storage',
    510: 'Not Extended',
}

RESPONSE_HEADERS_DICT = dict(zip(map(lambda x: x.upper(), RESPONSE_HEADERS), RESPONSE_HEADERS))
HEADER_X_POWERED_BY = ('X-Powered-By', 'test/0.1')
RE_RESPONSE_STATUS = re.compile(r'^\d\d\d(\ [\w\ ]+)?$')

def _to_str(s):

    if isinstance(s, str):
        return s
    if isinstance(s, unicode):
        return s.encode('utf-8')
    return str(s)

class Response:
	def __init__(self):
		self._status = '200 OK'
		self._response_headers = []
		
	@property
	def response_headers(self):
		return self._response_headers
		
	# def delete_cookie(self, name):
		# self.set_cookie(name, '__deleted__', expires=0)
		
	# def set_cookie(self, name, value, max_age=0, expires=None, path='/', domain=None, secure=False, http_only=True):
		# if hasattr(self, '_cookies'):
			# self._cookies = {}
		# res = ['%s=%s' % (name, value)]

		# if expires is not None:
			# res.append('Expires=%s' % expires)
		# elif isinstance(max_age, (int, long)):
			# res.append('Max-Age=%d' % max_age)

		# if domain:
			# res.append('Domain=%s' % domain)
		# if secure:
			# res.append('Secure')
		# if http_only:
			# res.append('HttpOnly')
		# self._cookies[name] = '; '.join(res)

	# @property
	# def cookie(self):
		# if hasattr(self, '_cookies'):
			# return self._cookies
		# else:
			# return ''

	def clear_header(self):
		del self._response_headers[:]

	def add_header(self, key, value):
		if key.upper() in RESPONSE_HEADERS_DICT.keys():
			self._response_headers.append((key, value))
		else:
			pass

	def del_header(self, key):
		index = 0 #array index
		for item in self._response_headers:
			if item[0] == key:
				del self._response_headers[index]
			else:
				index = index + 1

	@property
	def status_code(self):
		return int(self._status[:3])
		
	@property
	def status(self):
		return self._status
		
	@status.setter
	def status(self, value):
		if isinstance(value, (int, long)): #all number type
			if value >= 100 and value <= 999:
				status_value = RESPONSE_STATUSES.get(value, '')
				if status_value:
					self._status = '%d %s' % (value, status_value)
				else:
					self._status = str(value)
		elif isinstance(value, basestring): #basestring type
			if isinstance(value, unicode):
				value = value.encode('utf-8')
			if RE_RESPONSE_STATUS.match(value):
				self._status = value
			else:
				raise ValueError('Bad Response Code: %s' % value)
		else: #others type
			raise TypeError('Bad Type of Response Code.')

class Form:
	def __init__(self):
		pass

	@property
	def textbox(self):
		pass

	@property
	def password(self):
		pass

	@property
	def botton(self):
		pass

	@property
	def checkbox(self):
		pass

	@property
	def textarea(self):
		pass

	@property
	def dropdown(self):
		pass

	@property
	def radio(self):
		pass

class my_app:

	def __init__(self, urls=(), fvars={}):
		self._urls = urls
		self._fvars = fvars

	# def run(self, *middleware):
		# pass

	def wsgi(self, environ, start_response):
		""" The bottle WSGI-interface. """
		try:
			ctx.request = Request(environ)
			ctx.response = Response()
			ctx.response.clear_header()
			start_response(ctx.response.status, ctx.response.response_headers)
			router_table = Router(self._urls, self._fvars)
			return router_table.dispatch()
		except(KeyboardInterrupt, SystemExit, MemoryError):
			raise 'error'
		except Exception, e:
			del ctx.request
			del ctx.response
			raise 'Internet Error'

	def __call__(self, environ, start_response):
		return self.wsgi(environ, start_response)

def run(app = None, host = '127.0.0.1', port = 8086, debug = True, server = 'wsgiref'):
	if debug:
		from wsgiref.simple_server import make_server as start
		httpd = start(host, port, app)
		sa = httpd.socket.getsockname()
		print 'http://{0}:{1}/'.format(*sa)
		httpd.serve_forever()
	else:
		print('No Server')