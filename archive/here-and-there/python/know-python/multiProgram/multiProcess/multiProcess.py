#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
	multiprocessing 
	执行函数
'''
from multiprocessing import Process
def run_proc(name):
	print('Run child process %s (%s)...'% (name,os.getpid()))

if __name__=='__main__':
	print('Parent process %s.'% os.getpid())
	#创建子进程时，只需要传入一个执行函数和函数的参数
	p=Process(target=run_proc,args=('test',))
	print('Child process will start')
	#启动进程
	p.start()
	#等待子进程结束后在继续往下运行，通常用于进程间的同步
	p.join()
	print('Child process end.')
