#!/usr/bin/env python3

def fib(max):
	'''
		use generator to creat fib.
	'''
	a,b = 0,0,1
	for i in range(max):
		yield b
		a, b = b, a+b
	return 'done'
