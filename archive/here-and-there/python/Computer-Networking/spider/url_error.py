#!/usr/bin/env python2.7
import urllib2

request=urllib2.Request('https://www.XXXX.com')
try:
	urllib2.urlopen(request,timeout=10)
except urllib2.HTTPError,e:
	print e.code
	print e.reason


try:
	urllib2.urlopen(request,timeout=10)
except urllib2.HTTPError,e:
	print e.code
except urllib2.URLError,e:
	print e.reason
else:
	print "Ok"

try:
	urllib2.urlopen(request,timeout=10)
except urllib2.URLError,e:
	if hasattr(e,"code"):
		print e.code
	if hasattr(e,"reason"):
		print e.reason
else:
	print "OK"
