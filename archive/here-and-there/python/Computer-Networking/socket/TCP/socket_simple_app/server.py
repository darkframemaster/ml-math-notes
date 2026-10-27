#!/usr/bin/env python2.7

__author__ = 'darkframexue'

import socket
import socket, sys, threading  
    
__author__ = "darkframexue"

HOST = '127.0.0.1' #server IP
PORT = 18080 #server port

index_content = '''HTTP/1.X 200 ok	
Content-Type: text/html	
	

'''

file = open('index.html', 'r')
index_content += file.read()
file.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', PORT))
sock.listen(100)

while True:
	conn, addr = sock.accept()
	request = conn.recv(1024)
	method = request.split(' ')[0]
	src = request.split(' ')[1]
	
	print 'Connect by: ', addr
	print 'Request is:\n', request

	content = index_content

	conn.sendall(content)
	conn.close()
