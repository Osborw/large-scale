import signal
import sys
import aiohttp
import json
import os
import aiohttp
from main import settings

settings.get_config(os.path.dirname(os.path.realpath(__file__))+"\\config\\config.yaml")

def return_data(name):
	f=open(os.path.dirname(os.path.realpath(__file__))+"\\test_helper\\"+name)
	data=f.read()
	return data

class TestClass(object):
	async def test_index(self): #Checking index
		client = aiohttp.ClientSession()
		resp = await client.get('http://'+str(settings.config['host'])+':'+str(settings.config['port']))
		assert resp.status == 200

	async def test_add(self): #Basic Link Analysis
		client = aiohttp.ClientSession()
		resp = await client.post('http://'+str(settings.config['host'])+':'+str(settings.config['port'])+'/la',data=return_data("link_analysis_input1.json"))
		assert resp.status == 200

	async def test_remove(self): #Basic Crawling Delete 404 Error
		client = aiohttp.ClientSession()
		resp = await client.post('http://'+str(settings.config['host'])+':'+str(settings.config['port'])+'/crawling',data=return_data("crawling_input1.json"))
		assert resp.status == 200

	async def test_modify(self): #Basic Crawling Delete 301 Error
		client = aiohttp.ClientSession()
		resp = await client.post('http://'+str(settings.config['host'])+':'+str(settings.config['port'])+'/crawling',data=return_data("crawling_input2.json"))
		assert resp.status == 200

	async def test_add1(self): #Basic Link Analysis
		client = aiohttp.ClientSession()
		resp = await client.post('http://'+str(settings.config['host'])+':'+str(settings.config['port'])+'/la',data=return_data("link_analysis_input1.json"))
		assert resp.status == 200