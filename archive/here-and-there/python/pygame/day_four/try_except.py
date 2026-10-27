#!/usr/bin/env python2.7
s=raw_input("Enter a number:")
try:
	number=float(s)
except:
	number=0
answer=number*number
print(number,"*",number,"=",answer)

