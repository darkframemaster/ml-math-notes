#!/usr/bin/env python3


if __name__=='__main__':
	from test import *
	test=Test()

	try:
		_test()
	except:
		print("Cannot use import * to import function name as '_funcname'")

	try:
		__test()
	except:
		print("'__funcname' either")

	try:
		test.__test_func()
	except:
		print("Cannot use Non-public function name as:__funcname.")

	try:
		test=__Test()
	except:
		print("Cannot use Non-public class name as:__classname.")
