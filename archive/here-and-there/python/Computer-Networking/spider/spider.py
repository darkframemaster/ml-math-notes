#!/usr/bin/env python2.7
import socket
import urllib
import urllib2

class spider():
	url=''
	data=None
	user_agent=''
	referer=''
	headers=socket._GLOBAL_DEFAULT_TIMEOUT
	html=None

	def __init__(self,url,data,user_agent,referer,headers):
		self.url=url
		if(self.URLError()==False):
			print('urlError!!!')
			return False	
		self.data=data
		self.user_agent=user_agent
		self.referer=referer
		self.headers=headers
	
	def Get(self):
		data=urllib.urlencode(self.data)
		url=self.url+"?"+data
		self.html=urllib2.Request(url,None,self.headers)
		self.html=urllib2.urlopen(self.html)
		return self.html.read()

	def Post(self):
		data=urllib.urlencode(self.data)
		self.html=urllib2.Request(self.url,data,self.headers)
		self.html=urllib2.urlopen(self.html)
		return self.html.read()

	def Put(self):
		data=urllib.urlencode(self.data)
		self.html=urllib2.Request(self.url,data,self.headers)
		self.html.get_method=lambda:'PUT'
		self.html=urllib2.urlopen(self.html)
		return self.html.read()
		
	def Delete(self):
		data=urllib.urlencode(self.data)
		self.html=urllib2.Request(self.url,data,self.headers)
		self.html.get_method=lambda:'DELETE'
		self.html=urllib2.urlopen(self.html)
		return self.html.read()

	def set_Proxy(self):
		enable_proxy = True
		proxy_handler = urllib2.ProxyHandler({"http" : 'http://some-proxy.com:8080'})
		null_proxy_handler = urllib2.ProxyHandler({})
		if enable_proxy:
		    opener = urllib2.build_opener(proxy_handler)
		else:
		    opener = urllib2.build_opener(null_proxy_handler)
		urllib2.install_opener(opener)	
		
	def Debuglog(self):
		httpHandler=urllib2.HTTPHandler(debuglevel=1)
		httpsHandler=urllib2.HTTPHandler(debuglevel=1)
		opener=urllib2.build_opener(httpHandler,httpsHandler)
		urllib2.install_opener(opener)
		response=urllib2.urlopen(self.url)

	def URLError(self):
		self.html=urllib2.Request(self.url)
		try:
			urllib2.urlopen(self.html)		
		except	urllib2.URLError,e:
			print e.reason
			return True
		return False

url='http://202.118.65.20:8081/login.jsp'
data={'username':'','password':''}
user_agent='Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'
referer='http://202.118.68.128/'
headers={'User-Agent':user_agent,'Referer':referer}
page=spider()
page._init_(url,data,user_agent,referer,headers)
page.Get()
print(page)
page.Post()
print(page)
page.Put()
print(page)
page.Delete()
print(page)
page.Debuglog()






