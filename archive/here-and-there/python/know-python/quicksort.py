#!/usr/bin/env python3

from timeit import timeit

def quicksort(lst):
	if lst is None or len(lst) in (0,1):
		return lst
	else:
		return quicksort([x for x in lst[1:] if x<lst[0]])+[lst[0]]+quicksort([x for x  in lst[1:] if x>lst[0]])

if __name__=='__main__':
	print(timeit('quicksort([1,10,2,9,3,8,4,7,5,6])','from quicksort import quicksort',number=100))
	print(timeit('[1,10,2,9,3,8,4,7,5,6].sort()','from quicksort import quicksort',number=100))
	print('the function in python is really powerful!!!')
