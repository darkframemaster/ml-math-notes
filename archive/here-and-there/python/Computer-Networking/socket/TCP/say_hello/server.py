#!/usr/bin/env python2.7

__author = 'darkframexue'

import socket
import threading
import time

def request_handler(sock,addr):
	print('Accept new connection from %s:%s...'% addr)
	sock.send(b'Welcome!')
	while True:
		data=sock.recv(1024)
		time.sleep(1)
		if not data or data.decode('utf-8')=='exit':
			break
		sock.send(('Hello,%s!'% data).encode('utf-8'))
	sock.close()
	print('Connection from %s:%s closed.'% addr)

def server_start(link_ip,port_num):
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	
	# Bind the address and port for monitor(jianting).
	# "127.0.0.1" is the address of owners computer.
	# Choose a high port number like 18080.
	# Your need root right for port_number<1024.
	s.bind((link_ip,int(port_num)))
	s.listen(5)
	print('Waiting for connection...')
	
	while True:
		# Receive a connection
		sock,addr=s.accept()
		# Create a new thread for TCP link
		# We will use the client socket `sock`, but not `s`.
		t=threading.Thread(target=request_handler,args=(sock,addr))
		t.start()
	
if __name__ == '__main__':
	print("now start monitor!!!")
	server_start('127.0.0.1',9999)
