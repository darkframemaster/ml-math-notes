#!/usr/bin/env python2.7

import pygame
from pygame.locals import *

pygame.init()
screen=pygame.display.set_mode((600,500))
pygame.display.set_caption("Drawing Rectangles")
pos_x=300
pos_y=250
vel_x=2
vel_y=1
while True:
	for event in pygame.event.get():
		if event.type in (QUIT,KEYDOWN):
			sys.exit()
	
	screen.fill((0,0,200))

	#move the rectangle
	pos_x+=vel_x
	pos_y+=vel_y

	#keep rectangle on the screen
	if pos_x>600 or pos_x<0:
		vel_x=-vel_x
	if pos_y>500 or pos_y<0:
		vel_y=-vel_y

	#draw the rectangle
	color=255,255,0
	width=0 #solid fill
	pos=pos_x,pos_y,10,10	#sames like the last two values means the width of the rectangle
	pygame.draw.rect(screen,color,pos,width)

	pygame.display.update()
