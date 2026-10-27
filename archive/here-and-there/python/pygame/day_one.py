#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

#day_two code
#OOP:python 

class Bug():
	legs=0
	distance=0
	
	def _init_(self,name,legs):
		self.name=name
		self.legs=legs

	def _init_(self,name="xuehao",legs=2):
		self.name=name
		self.legs=legs
	
	def Walk(self):
		self.distance+=1

	def Walk(self,distance=2):
		self.distance+=distance	

	def ToString(self):
		return self.name+" has "+str(self.legs)+" legs "+" and taken "+str(self.distance)+" steps."
	
	def GetDistance(self):
		return self.distance

	def SetDistance(self,value):
		self.distance=value
	

#before the variable there must be a key word `self`
#Polymorphism(duo tai) is allowed in class definition

myself=Bug()
myself._init_("xuehao",2)
print(myself.ToString())
myself.Walk()
print(myself.ToString())

myself.distance=100
print(myself.ToString())
myself.SetDistance(200)
print(myself.GetDistance())
