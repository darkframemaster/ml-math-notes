#!/usr/bin/env python2.7
import socket
from socket import *
serverName='127.0.0.1'
serverPort=12000
clientSocket=socket(AF_INET,SOCK_DGRAM)
message=raw_input('input lowercase sentence:')
clientSocket.sendto(message,(serverName,serverPort))
modifiedMessage,serverAddress=clientSocket.recvfrom(2048)
print(modifiedMessage)
clientSocket.close()

