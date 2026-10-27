#!/usr/bin/env python2.7
import socket 
from socket import *


while True:
	#each link need to recreate connection
	serverName='127.0.0.1'
	serverPort=12001
	clientSocket=socket(AF_INET,SOCK_STREAM)
	clientSocket.connect((serverName,serverPort))
	
	sentence=raw_input("input lowercase sentence:")

	clientSocket.send(sentence)
	modifiedSentence=clientSocket.recv(1024)
	print("From server:%s"% modifiedSentence)
	clientSocket.close()
