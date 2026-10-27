#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from PIL import Image
import argparse

#命令行输入参数处理
parser=argparse.ArgumentParser()

parser.add_argument('file')		#输入文件
parser.add_argument('-o','--output')	#输出文件
parser.add_argument('--width',type=int,default=80)	#输出字符画宽
parser.add_argument('--height',type=int,default=80)	#输出字符画高

#获取参数
args=parser.parse_args()

IMG=args.file
WIDTH=args.width
HEIGHT=args.height
OUTPUT=args.output

ascii_char = list("oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'")

def get_char(r,b,g,alpha=256):
	if alpha==0:
		return ' '
	length=len(ascii_char)
	gray=int(0.2126*r + 0.7152*g + 0.0722*b)
	
	if gray>200:
		return ' '
	elif gray>150:
		return ' '
	elif gray>100:
		return ':'
	elif gray<50:
		return '0'
	else:
		return '*'
	'''	
	elif gray<70:
		return '$'
		
	elif gray<=100:
		return '*'
	'''
	unit=(256.0 + 1)/length
	return ascii_char[int(gray/unit)]

if __name__=="__main__":
	im=Image.open(IMG)
	im=im.resize((WIDTH,HEIGHT),Image.NEAREST)
	
	alist=[]
	txt=""
	for i in range(HEIGHT):
		for j in range(WIDTH):
			txt+=get_char(*im.getpixel((j,i)))	
		txt+='\n'
	print(txt)

	if OUTPUT:
		with open(OUTPUT,'w') as f:
			f.write(txt)
	else:
		with open(str(IMG)[:-4]+".txt",'w') as f:
			f.write(txt)
