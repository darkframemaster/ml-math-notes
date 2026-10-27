#!/usr/bin/env python2.7
import pygame
from pygame.locals import *
pygame.init()
screen=pygame.display.set_mode((600,500))
pygame.display.set_caption("Drawing Circles")
while True:
	for event in pygame.event.get():
		if event.type in (QUIT,KEYDOWN):
			sys.exit()

	screen.fill((0,0,200))

	#draw a circle		
	#we draw things here
	color =255,255,0	
	position=300,250	#center position
	radius=100		#radius of the circle
	width=10		#width of the line
	pygame.draw.circle(screen,color,position,radius,width)

	pygame.display.update()	#reflash
