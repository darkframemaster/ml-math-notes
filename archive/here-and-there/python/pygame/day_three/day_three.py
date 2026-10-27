#!/usr/bin/env python2.7

import pygame
from pygame.locals import *
white=255,255,255
blue=0,0,255
pygame.init()

#set screen
screen=pygame.display.set_mode((600,500))

#set word
myfont=pygame.font.Font(None,60)
textImage=myfont.render("Hello pygame",True,white)


#while -a loop of flashing the screen
while True:
	for event in pygame.event.get():
		if event.type in (QUIT,KEYDOWN):
			sys.exit()
	#reflash the screen
	screen.fill(blue)
	screen.blit(textImage,(100,100))  		
	pygame.display.update()
