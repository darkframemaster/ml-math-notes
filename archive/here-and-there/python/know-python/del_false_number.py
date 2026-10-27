#!/usr/bin/env python3

'''
input two same length list:
one for number
one for boolean

keep the number when True and set the number for 0 when False.

'''

__author__ = "darkframexue"


def del_false_number(a,b):
	return list(map(lambda x,y: x if y else 0, a, b))


if __name__== "__main__":

	a = range(0,10)
	b = [1,0,0,1,0,1,0,1,1,0]
	print(del_false_number(a,b))

