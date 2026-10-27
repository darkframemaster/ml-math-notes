#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import functools

from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "github"
MONGO_COL = "user"

col = None
db = None
client = None

def connect():
	global client, db, col
	client = MongoClient(MONGO_HOST, MONGO_PORT)
	db = client[MONGO_DB]
	col = db[MONGO_COL]

def close():
	client.close()

def with_mongo_connect(func):
	@functools.wraps(func)
	def wrapper(*args, **kw):
		connect()
		ret = func(*args, **kw)
		close()
		return ret
	return wrapper

@with_mongo_connect
def exist(user_id):
	doc = col.find_one({'id': user_id})
	if doc is not None:
		return True
	return False

@with_mongo_connect
def insert_if_not_exist(doc):
	if exist(doc['id']):
		return False
	else:
		col.insert(doc)
		close()
		return True

@with_mongo_connect
def insert_one_doc(doc):
	try:
		col.insert(doc)
		close()
		return True
	else:
		return False
