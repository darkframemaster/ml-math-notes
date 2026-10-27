#!/usr/bin/env python2.7
import urllib
import urllib2

def get_html(url,data=None):
	request=urllib2.Request(url,data)
	html=urllib2.urlopen(request)
	html=html.read()
	return html

#post
values={"username":"darkframemaster","password":""}
data=urllib.urlencode(values)
url="https://github.com/login"
print(get_html(url,data))

#get
values={"username":"darkframemaster","password":""}
data=urllib.urlencode(values)
url="https://github.com/login"
geturl=url+"?"+data
print(get_html(geturl))

