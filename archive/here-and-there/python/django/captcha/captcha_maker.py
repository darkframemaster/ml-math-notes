#!/usr/bin/env python
#-*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import os, sys
import time, random
import string
import six

try:
	from cStringIO import StringIO
except ImportError:
	from io import BytesIO as StringIO

from config import *
from helpers import get_noise_func_list, get_filter_func_list



def make_valid_pic(pic_name):
	for pic_type in IMG_TYPES:
		if pic_type in pic_name.lower():
			return pic_name
	return pic_name + '.png'

def get_size(font, text):
	if hasattr(font, 'getoffset'):
		return tuple([x + y for x, y in zip(font.getsize(text), font.getoffset(text))])
	else:
		return font.getsize(text)
	
def make_img(size):
	image = Image.new('RGB', size, CAPTCHA_BACKGROUND_COLOR)
	return image

def captcha(pic_name, game_type = 'dota2'):
	'''
	Captcha
	'''
	pic_name = make_valid_pic(pic_name)
	pic_path = PIC_PATH + pic_name if os.path.exists(PIC_PATH) else ''
	font_path = FONT_PATH + FONT_FILE if os.path.exists(FONT_PATH) else '' 

	if font_path.lower().strip().endswith('ttf'):
		font = ImageFont.truetype(font_path, 22)
	else:
		font = ImageFont.load(font_path)
	
	if game_type:
		text = random.choice(HEROS[game_type])
	else:
		text = ''.join(random.sample(string.letters + string.digits, 4))
	size = get_size(font, text)
	size = (size[0] * 2, int(size[1] * 1.4))

	image = make_img(size)
	xpos = 2
	from_top = 4

	char_list = [char for char in text]
	for char in char_list:
		print char
		fg_image = Image.new('RGB', size, CAPTCHA_FOREGROUND_COLOR)
		char_image = Image.new('L', get_size(font, ' %s '%char), '#000000')
		char_draw = ImageDraw.Draw(char_image)
		char_draw.text((0, 0), ' %s '%char, font = font, fill = '#ffffff')
		if CAPTCHA_LETTER_ROTATION:
			char_image = char_image.rotate(random.randrange(*CAPTCHA_LETTER_ROTATION), expand=0, resample=Image.BICUBIC)
		
		char_image = char_image.crop(char_image.getbbox())
		mask_image = Image.new('L', size)

		mask_image.paste(char_image, (xpos, from_top, xpos+char_image.size[0], from_top+char_image.size[1]))
		size = mask_image.size
		
		image = Image.composite(fg_image, image, mask_image)
		xpos = xpos + 2 + char_image.size[0]

	# centering captcha on the image
	tmp_img = make_img(size)
	tmp_img.paste(image, (int((size[0] - xpos) / 2), int((size[1] - char_image.size[1]) / 2 - from_top)))

	image = tmp_img.crop((0, 0, size[0], size[1]))
	draw = ImageDraw.Draw(image)

	image.save('image', SAVE_AS)
	for func in get_noise_func_list():
		draw = func(draw, image)
	image.save('image_noise', SAVE_AS)
	
	for func in get_filter_func_list():
		image = func(image)
	
	image.save(pic_path, SAVE_AS)
	return image, text

if __name__ == '__main__':
	while True:
		pic_name = raw_input('input a pic_name:\n')
		captcha(pic_name)
