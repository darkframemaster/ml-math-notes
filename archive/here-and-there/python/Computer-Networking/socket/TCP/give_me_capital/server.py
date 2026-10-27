#!/usr/bin/env python2.7
import socket 
from socket import *

serverPort=12001
serverSocket=socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print("the server is ready ro receive")

while True:
	connectionSocket,addr=serverSocket.accept()
	sentence=connectionSocket.recv(1024)
	print(sentence)
	capitalizedSentence=sentence.upper()
	connectionSocket.send(capitalizedSentence)
	connectionSocket.close()
