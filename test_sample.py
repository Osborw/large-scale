import signal
import sys
import aiohttp
import json
import os
import requests
from main import settings

#settings.get_config(os.path.dirname(os.path.realpath(__file__))+"/config/config.yaml")

host = "green-eth.cs.rpi.edu"
port = str(5433)

def return_data(name):
	f=open(os.path.dirname(os.path.realpath(__file__))+"/test_helper/"+name)
	data=f.read()
	return data

class TestClass(object):
	# async def test_index(self): #Checking index
	# 	client = aiohttp.ClientSession()
	# 	resp = await client.get('http://'+host+':'+port)
	# 	assert resp.status == 200

	# async def test_add(self): #Basic Link Analysis
	# 	client = aiohttp.ClientSession()
	# 	resp = await client.post('http://'+host+':'+port+'/la',data=return_data("link_analysis_input1.json"))
	# 	assert resp.status == 200

	# async def test_remove(self): #Basic Crawling Redirect 403 Error
	# 	client = aiohttp.ClientSession()
	# 	resp = await client.post('http://'+host+':'+port+'/crawling',data=return_data("crawling_input1.json"))
	# 	assert resp.status == 200

	# async def test_modify(self): #Basic Crawling Delete 404 Error
	# 	client = aiohttp.ClientSession()
	# 	resp = await client.post('http://'+host+':'+port+'/crawling',data=return_data("crawling_input2.json"))
	# 	assert resp.status == 200

	# async def test_add1(self): #Basic Text Transformation
	# 	client = aiohttp.ClientSession()
	# 	resp = await client.post('http://'+host+':'+port+'/tt',data=return_data("text_transformation1.json"))
	# 	assert resp.status == 200

	# async def test_add2(self): #Basic Text Transformation
	# 	client = aiohttp.ClientSession()
	# 	resp = await client.post('http://'+host+':'+port+'/tt',data=return_data("text_transformation2.json"))
	# 	assert resp.status == 200

	# async def test_get1(self): #Basic Text Transformation
	# 	client = aiohttp.ClientSession()
	# 	resp = await client.post('http://'+host+':'+port+'/querying',data=return_data("querying1.json"))
	# 	assert resp.status == 200

	# async def test_add3(self): #Basic Text Transformation
	# 	client = aiohttp.ClientSession()
	# 	resp = await client.post('http://'+host+':'+port+'/la',data=return_data("link_analysis_input2.json"))
	# 	assert resp.status == 200

	def test_index(self): #Checking index		
		resp = requests.get('http://'+host+':'+port)
		assert resp.status_code == 200

	def test_add(self): #Basic Link Analysis
		resp = requests.post('http://'+host+':'+port+'/la',data=return_data("link_analysis_input1.json"))
		assert resp.status_code == 200

	def test_remove(self): #Basic Crawling Redirect 403 Error
		resp = requests.post('http://'+host+':'+port+'/crawling',data=return_data("crawling_input1.json"))
		assert resp.status_code == 200

	def test_modify(self): #Basic Crawling Delete 404 Error
		resp = requests.post('http://'+host+':'+port+'/crawling',data=return_data("crawling_input2.json"))
		assert resp.status_code == 200

	def test_add1(self): #Basic Text Transformation
		resp = requests.post('http://'+host+':'+port+'/tt',data=return_data("text_transformation1.json"))
		assert resp.status_code == 200

	def test_add2(self): #Basic Text Transformation
		resp = requests.post('http://'+host+':'+port+'/tt',data=return_data("text_transformation2.json"))
		assert resp.status_code == 200

	def test_get1(self): #Basic Text Transformation
		resp = requests.post('http://'+host+':'+port+'/querying',data=return_data("querying1.json"))
		assert resp.status_code == 200

	def test_add3(self): #Basic Text Transformation
		resp = requests.post('http://'+host+':'+port+'/la',data=return_data("link_analysis_input2.json"))
		assert resp.status_code == 200