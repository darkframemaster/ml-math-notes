#!/usr/bin/env python3.4
#-*- coding:utf-8 -*-

#继承
#来自父类的冲突变量和方法在继承顺序中具有优先性，当调用一个基类的构造函数或任何方法的时候，使用super()来引用
class Point():
	x=0.0
	y=0.0

	def _init_(self,x,y):
		self.x=x
		self.y=y
		print("Point constructor")

	def ToString(self):
		return "{x:"+str(self.x)+",y:"+str(self.y)+"}"

class Circle(Point):
	radius=0.0

	def _init_(self,x,y,radius):
		super()._init_(x,y)
		self.radius=radius
		print("Circle constructor")

	def CaleCircum(self):
		return 2*3.14159*self.radius

	def ToString(self):
		return super().ToString()+",{RADIUS="+str(self.radius)+"}"


p=Point()
p._init_(10,20)
print(p.ToString())

c=Circle()
c._init_(100,100,50)
print(c.CaleCircum())
print(c.ToString())

#多继承要慎用

print("多继承慎用")

class Size():
	width=0.0
	height=0.0

	def _init_(self,width,height):
		self.width=width
		self.height=height
		print("Size constructor")

	def ToString(self):
		return "{WIDTH="+str(self.width)+",HEIGHT="+str(self.height)+"}"
	
class Rectangle(Point,Size):
	def _init_(self,x,y,width,height):
		Point._init_(self,x,y)
		Size._init_(self,width,height)
		print("Rectangle construtor")

	def ToString(self):
		return Point.ToString(self)+","+Size.ToString(self)

s=Size()
s._init_(80,70)
print(s.ToString())


r=Rectangle()
r._init_(200,250,40,50)
print(r.ToString())
