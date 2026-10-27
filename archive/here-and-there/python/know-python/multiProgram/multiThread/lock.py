#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import time,threading

#asume this is your money in the bank system
balance=0
#get a lock
lock=threading.Lock()

def change_it(n):
	#save first and then checkout,the balance should be 0
	global balance
	balance=balance+n
	balance=balance-n

def run_thread(n):
	for i in range(100000):
		#get a lock
		lock.acquire()
		try:
			change_it(n)
		finally:
			#release after use
			lock.release()

for i in range(20):
	t1=threading.Thread(target=run_thread,args=(5,))
	t2=threading.Thread(target=run_thread,args=(8,))
	t1.start()
	t2.start()

t1.join()
t2.join()
print(balance)

