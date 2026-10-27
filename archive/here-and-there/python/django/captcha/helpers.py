#!/usr/bin/env python
#-*- coding:utf-8 -*-

import random

from config import CAPTCHA_FOREGROUND_COLOR

def noise_dots(draw, image):
	size = image.size
	for p in range(int(size[0] * size[1] * 0.1)):
		draw.point(
			(random.randint(0, size[0]), random.randint(0, size[1])),
			fill = CAPTCHA_FOREGROUND_COLOR,
			)
	return draw

def noise_arcs(draw, image):
	size = image.size
	draw.arc(
		[-20, -20, size[0], 20],
		0,
		295,
		fill = CAPTCHA_FOREGROUND_COLOR,
		)
	draw.line(
		[-20, 20, size[0] + 20, size[1] - 20],
		fill = CAPTCHA_FOREGROUND_COLOR,
		)
	draw.line(
		[-20, 0, size[0] + 20, size[1]],
		fill = CAPTCHA_FOREGROUND_COLOR,
		)
	return draw

def post_smooth(image):
	try:
		import ImageFilter
	except ImportError:
		from PIL import ImageFilter
	return image.filter(ImageFilter.SMOOTH)

def get_noise_func_list():
	return [noise_dots, noise_arcs]

def get_filter_func_list():
	return [post_smooth]
