#!/usr/bin/env python2.7
import sys,pygame
from pygame.locals import *

#main program begins
pygame.init()
screen=pygame.display.set_mode((600,500))
pygame.display.set_caption("The Trivia Game")
font1=pygame.font.Font(None,40)
font2=pygame.font.Font(None,24)
white=255,255,255
cyan=0,255,255
yellow=255,255,0
purple=255,0,255
green=0,255,0
red=255,0,0

#other founction
def print_text(font,x,y,text,color=(255,255,255),shadow=True):
	if shadow:
		imgText=font.render(text,True,(0,0,0))
		screen.blit(imgText,(x-2,y-2))
	imgText=font.render(text,True,color)
	screen.blit(imgText,(x,y))

class Trivia():
	def _init_(self,filename):
		self.data=[]		#question list for all
		self.current=0		#current position	
		self.total=0		#lenth of the list
		self.correct=0		#correct answer of current question
		self.score=0		#score
		self.scored=False	#correcr
		self.failed=False	#incorrect
		self.wronganswer=0	#wrong answer
		self.colors=[white,white,white,white]
		#read trivia data from file
		try:		
			f=open(filename,"r")
		except:
			sys.exit()
		trivia_data=f.readlines()
		f.close()
		#count and clean up trivia data
		for text_line in trivia_data:
			self.data.append(text_line.strip())
			self.total+=1
	
	def show_question(self):
		print_text(font1,210,5,"TRIVIA GAME")
		print_text(font2,190,500-20,"Press Keys (1-4) To Answer",purple)
		print_text(font2,530,5,"SCORE",purple)
		print_text(font2,550,25,str(self.score),purple)
	
		#get correct answer out of data(first)
		self.correct=int(self.data[self.current+5])

		#display question
		question=(self.current)%5+1
		print_text(font1,5,80,"QUESTION "+str(question))
		print_text(font2,20,120,self.data[self.current],yellow)

		#respond to correct answer
		if self.scored:
			self.colors=[white,white,white,white]
			self.colors[self.correct-1]=green
			print_text(font1,230,380,"CORRECT!",green)
			print_text(font2,170,420,"Press Enter For Next Question",green)
		elif self.failed:
			self.colors=[white,white,white,white]
			self.colors[self.wronganswer-1]=red
			self.colors[self.correct-1]=green
			print_text(font1,220,380,"INCORRECT!",red)
			print_text(font2,170,420,"Press Enter For Next Question",red)
	
		#display
		print_text(font1,5,170,"ANSWERS")
		print_text(font2,20,210,"1-"+self.data[self.current+1],self.colors[0])
		print_text(font2,20,240,"2-"+self.data[self.current+2],self.colors[1])
		print_text(font2,20,270,"3-"+self.data[self.current+3],self.colors[2])
		print_text(font2,20,300,"4-"+self.data[self.current+4],self.colors[3])

	def handle_input(self,number):
		if not self.scored and not self.failed:
			if number==self.correct:
				self.scored=True
				self.score+=1
			else:
				self.failed=True
				self.wronganswer=number

	def next_question(self):
		if self.scored or self.failed:
			self.scored=False
			self.failed=False
			self.correct=0
			self.colors=[white,white,white,white]
			self.current+=6			
			if self.current>=self.total:
				self.current=0
				self.score=0
				return False
			else: return True

#load the trivia data file
trivia =Trivia()
trivia._init_("trivia_data.txt")
if_next=True

#repeating loop
while True:
	if(if_next):
		for event in pygame.event.get():
			if event.type==QUIT:
				sys.exit()
			elif event.type==KEYUP:
				if event.key==pygame.K_ESCAPE:
					sys.exit()
				elif event.key==pygame.K_1:
					trivia.handle_input(1)
				elif event.key==pygame.K_2:
					trivia.handle_input(2)
				elif event.key==pygame.K_3:
					trivia.handle_input(3)
				elif event.key==pygame.K_4:
					trivia.handle_input(4)
				elif event.key==pygame.K_RETURN:
					if_next=trivia.next_question()
				else: sys.exit()
		#clear the screen
			screen.fill((0,0,200))
		#display trivia date
			trivia.show_question()
			pygame.display.update()	
	else:
		screen.fill((0,0,200))
		print_text(font2,20,210,"Do you want to play again?(y/n)",green)
		pygame.display.update()				
		for event in pygame.event.get():
			if event.type==QUIT:
				print("QUIT")
				sys.exit()
			elif event.type==KEYUP:
				if event.key==pygame.K_1:
					print("what the fuck!!")
					trivia.current=0
					trivia.score=0
					if_next=True			
					trivia.show_question()
				else: 
					print("exit!")
					sys.exit()
			screen.fill((0,0,200))
			trivia.show_question()
			pygame.display.update()	


