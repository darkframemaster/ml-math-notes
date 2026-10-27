#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

BASE_PATH = os.path.abspath(os.path.dirname(__file__)) + '/static'
FONT_PATH = BASE_PATH + '/font/'
PIC_PATH  = BASE_PATH + '/pic/'
FONT_FILE = 'Consolas.ttf'
IMG_TYPES = ['png']
SAVE_AS   = "PNG"

HEROS = {
	'dota2':[
		'axe',
		'bane',
		'bone',
		'chen',
		'dirge',
		'enig',
		'fur',
		'goblin',
		'hus',
		'jugg',
		'kael',
		'kotl',
		'kunkka',
		'lich',
		'lina',
		'lion',
		'loa',
		'lucifer',
		'luna',
		'lyc',
		'mag',
		'medusa',
		'meepo',
		'mor',
		'N\'aix',
		'naga',
		'nec',
		'panda',
		'pom',
		'puck',
		'pudge',
		'pugna',
		'qop',
		'razor',
		'sil',
		'sniper',
		'snk',
		'spe',
		'storm',
		'sven',
		'thd',
		'tiny',
		'veno',
		'vip',
		'vis',
		'zeus'
		],
	'lol':[u'恶魔法师',]
}
CAPTCHA_FOREGROUND_COLOR = '#001100'
CAPTCHA_BACKGROUND_COLOR = '#ffffff'
CAPTCHA_LETTER_ROTATION = (-35, 35)
CAPTCHA_FONT_SIZE = 33
