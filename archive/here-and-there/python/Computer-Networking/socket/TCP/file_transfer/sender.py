#!/usr/bin/env

__author__ = 'darkframexue'

import socket

host = raw_input('input a host name:')
port = raw_input('input a port number:')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	client.connect((host, int(port)))
except Exception as e:
	print e
	exit('cannot build connection for the host, check your input!')

def file_reader(file_name):
	content = ''
	while True:
		try:
			with open(file_name, 'r') as f:
				content = f.read()
				break
		except IOError as e:
			file_name = raw_input(('file %s does not exists,'
			'input another name, '
			'or input "exit" to quit.') % file_name)
			if not file_name or file_name == 'exit':
				break
	return content

def add_file_name(file_name, content):
	return file_name + '\t\n' + content

def main():
	read_name = raw_input('file name you want to send:')
	save_name = raw_input('file name you want to save to:')
	save_name = save_name if save_name else read_name
	
	content = file_reader(read_name)
	if not content:
		return
	else:
		content = add_file_name(save_name, content)
	
	client.send(content)
	client.send('\t\n\n')
	print client.recv(1024)
	client.close()

if __name__ == '__main__':
	main()
