#!/usr/bin/env python3.4
import re

list_test=[1,2,3,4,4]
top=list_test.pop()
print(top)
print(list_test)

def swarp(station):
	return "haha"

Dict={'0':swarp(5),'1':"you"+"id"}
print(Dict)

Input=input('input:')
Stack=['0']
Stack_value=['0']
list_input=[]
list_number=[]

lenth=0
p_number = re.compile("(\d+)")
for match in p_number.finditer(Input):	#输入处理
		number=match.group(1)
		lenth=lenth+len(number)	#记录当前Input的位置 
		if number is None:	
			print("input error! no number found!")
			Input=input('please input again:')
		else:
			list_input.append('id')# list_input 中用id代替number 对应LR表 
			list_number.append(float(number))# list_number 中压入数字
			while(lenth<len(Input)):#扫描后面的串
				if Input[lenth] in ['+','*','(',')','$']:#如果有操作符
					list_input.append(Input[lenth]) #压入	
					list_number.append(Input[lenth])
					lenth=lenth+1
				else: 		
					break					

print(list_input)
print(list_number)
					


