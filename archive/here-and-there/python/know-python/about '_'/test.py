#!/usr/bin/env python3

print(__name__)

''' '_' in functions'''
def _test():
	print('func _test')

def __test():	
	print('func __test')

''' '_' in functions in class '''
class Test:
	def __init__(self):
		self._test_param_one='_test_param'
		self.__test_param_two='__test_param'	
	
	def __test_func(self):
		print(self._test_param_one)
		print(self.__test_param_two)
		print('_test_func')

''' '_' in class '''
class __Test__:
	def __init__(self):
		print('class __Test__')

if __name__=='__main__':
	_test()
	__test()
