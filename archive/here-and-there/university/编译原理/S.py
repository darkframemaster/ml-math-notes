#!/usr/bin/env python3.4
#!-*- coding:utf-8 -*-
import re

#function:
def get_value(top):#这里给的top是栈顶元素的栈，最顶端的最靠前
	#print('归约进行的value运算',top)
	#ans为中间语句
	if len(top)==1:
		#ans=str(top[-1])	
		ans=None
		return top[-1],ans
	elif top[0]==')':
		#ans='('+top[1]+')'
		ans=None		
		return top[1],ans
	elif top[1]=='+':
		ans=str(top[0])+'+'+str(top[-1])
		return top[0]+top[-1],ans
	else:
		ans=str(top[0])+'*'+str(top[-1])
		return top[0]*top[-1],ans


number_pos=0#用于计数现在到list_number里面的那个数	
def s(ope,num):#将操作符和状态压入
	global Stack
	global Stack_value
	global list_input
	global list_number
	global COUNT
	global number_pos

	if COUNT<len(list_input):
		COUNT=COUNT+1
	
	#语法栈
	Stack.append(ope)
	Stack.append(num)
	
	#语义栈
	if ope=='id':
		if(number_pos>len(list_number)):
			print('list_number error!')
		Stack_value.append(list_number[number_pos])
		number_pos=number_pos+1
		Stack_value.append(num)
	else:
		Stack_value.append(ope)
		Stack_value.append(num)

	if COUNT<len(list_input):
		print("移进:"+ope+'\t\t',   Stack, '\t',Stack_value ,'\t'+'next：'+list_input[COUNT])
	else:	
		print("移进:"+ope+'\t\t',   Stack, '\t',Stack_value ,'\t'+'next：'+list_input[COUNT-1])


def r(num):	#num为归约时使用的表达式		
	global Stack
	global Stack_value
	global list_input
	global list_number
	global LR_Table
	global list_simlag
	top=[]	#保存Stack_value每次归约时弹出的栈顶元素
	
	if(num==6):		#计算pop的次数
		pop_time=1
	else:
		pop_time=len(method[str(num)])-3

	while(pop_time>0):	#弹出
		#语法栈
		Stack.pop()
		Stack.pop()
		
		#语义栈		
		Stack_value.pop()
		top.append(Stack_value.pop())#将栈顶的元素复制给top
		pop_time=pop_time-1
	
	value,simlag=get_value(top)# get_value()为计算终结符value的方法，get_value返回value和中间语句
	Stack.append(method[str(num)][0])#压入非终结符
	Stack_value.append(value)#压入非终结符对应的value.
	if simlag is not None:	#DAG优化 	
		simlag="t"+str(len(list_simlag)+1)+'='+simlag#生成中间语句
		list_simlag.append(simlag)#保存中间语句		

	if(LR_Table[str(Stack[-2])][str(Stack[-1])] is not None): #能不能进行归约,有没有对应的状态
		Stack_value.append(LR_Table[str(Stack[-2])][str(Stack[-1])])#压入数值
		Stack.append(LR_Table[str(Stack[-2])][str(Stack[-1])])#压入状态	
	else:
		print("归约:error")

	print("归约:"+method[str(num)]+'\t\t',   Stack ,'\t' , Stack_value ,'\t'+'next：'+list_input[COUNT])

#data
method={'1':'E->E+T','2':'E->T','3':'T->T*F','4':'T->F','5':'F->(E)','6':'F->id'}
	
LR_Table={
'0':{'id':'s(5)','+':None,'*':None,'(':'s(4)',')':None,'$':None,'E':'1','T':'2','F':'3'},
'1':{'id':None,'+':'s(6)','*':None,'(':'s(4)',')':None,'$':'acc','E':None,'T':None,'F':None},
'2':{'id':None,'+':'r(2)','*':'s(7)','(':None,')':'r(2)','$':'r(2)','E':None,'T':None,'F':None},
'3':{'id':None,'+':'r(4)','*':'r(4)','(':None,')':'r(4)','$':'r(4)','E':None,'T':None,'F':None},
'4':{'id':'s(5)','+':None,'*':None,'(':'s(4)',')':None,'$':None,'E':'8','T':'2','F':'3'},
'5':{'id':None,'+':'r(6)','*':'r(6)','(':None,')':'r(6)','$':'r(6)','E':None,'T':None,'F':None},
'6':{'id':'s(5)','+':None,'*':None,'(':'s(4)',')':None,'$':None,'E':None,'T':'9','F':'3'},
'7':{'id':'s(5)','+':None,'*':None,'(':'s(4)',')':None,'$':None,'E':None,'T':None,'F':'10'},
'8':{'id':None,'+':'s(6)','*':None,'(':None,')':'s(11)','$':None,'E':None,'T':None,'F':None},
'9':{'id':None,'+':'r(1)','*':'s(7)','(':None,')':'r(1)','$':'r(1)','E':None,'T':None,'F':None},
'10':{'id':None,'+':'r(3)','*':'r(3)','(':None,')':'r(3)','$':'r(3)','E':None,'T':None,'F':None},
'11':{'id':None,'+':'r(5)','*':'r(5)','(':None,')':'r(5)','$':'r(5)','E':None,'T':None,'F':None},
}

legal_operator=['0','1','2','3','4','5','6','7','8','9','*','+','(',')','$']

#main program
Input=input('input:')

while(True):
	if(Input[-1]!='$'):
		print('please end with "$"!')
		Input=input('input again:')
	else:
		break

for i in Input:
	if i in legal_operator:
		continue	
	else:
		print('unexpected operator:',i)
		exit()
	

Stack=['0']#语法栈
Stack_value=['0']#语义栈
list_input=[]#用于存储输入的语法串
list_number=[]#用于存储输入中的数字
list_simlag=[]#用于存储中间语言

lenth=0
p_number = re.compile("(\d+)")

#输入处理
while(lenth<len(Input)):
	if Input[lenth] in ['+','*','(',')','$']:#如果有操作符
		list_input.append(Input[lenth]) #压入	
		#list_number.append(Input[lenth])
		lenth=lenth+1
	else: 		#######如果不是操作符（那么就是数字），跳出循环
		break

for match in p_number.finditer(Input):	
		number=match.group(1)
		lenth=lenth+len(number)	#记录当前Input的位置 ，加上数字的长度
		if number is None:	
			print("input error! no number found!")
			exit()
		else:
			list_input.append('id')# list_input 中用id代替number 对应LR表 
			list_number.append(int(number))# list_number 中压入数字
			while(lenth<len(Input)):#扫描后面的串
				if Input[lenth] in ['+','*','(',')','$']:#如果有操作符
					list_input.append(Input[lenth]) #压入	
					#list_number.append(Input[lenth])
					lenth=lenth+1
				else: 		#######如果不是操作符（那么就是数字），直接跳过
					break					

print(list_input)
print(list_number)

COUNT=0
while(True):		#循环检查
	if COUNT<len(list_input):	
		i=list_input[COUNT]#i是下一个操作符
		#print(Stack[-1],i)
	if(LR_Table[Stack[-1]][i]==None):#查栈顶元素和下一个操作符的操作 如果是none那么错误 如果是acc结束 否则看具体进行什么操作。
		print('error! unexpected word:',i)
		exit()
		COUNT=COUNT+1	#就算错了，也后移一位，继续语法分析
	elif(LR_Table[Stack[-1]][i]=='acc'):#正确结束的标志
		print('accept!')
		print('answer is :' , Stack_value[-2])
		break		
		#exit()
	else:#分析进行什么操作，并计算出操作符和操作的状态
		if((LR_Table[Stack[-1]][i][0])=='s'):
			if LR_Table[Stack[-1]][i][3]==')':
				s(i,LR_Table[Stack[-1]][i][2])
			else:
				s(i,LR_Table[Stack[-1]][i][2]+LR_Table[Stack[-1]][i][3])
		elif((LR_Table[Stack[-1]][i][0])=='r'):
			r(int(LR_Table[Stack[-1]][i][2]))

#输出中间语句:
print("\n中间语句:\n",list_simlag)
