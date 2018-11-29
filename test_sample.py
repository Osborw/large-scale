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

	#All of these test cases assume that the database is initialized to defaults.

	#------------------------#
	# Empty Data Transmitted #
	#------------------------#

	def test_CRAWLING_INCOMPLETE_INPUT(self):
		resp = requests.post('http://'+host+':'+port+'/crawling',data=return_data("incomplete.json"))
		print("RETURN VALUE:"+json.loads(resp.text)["message"])
		assert resp.status_code == 500
		
	def test_LINK_ANALYSIS_INCOMPLETE_INPUT(self):
		resp = requests.post('http://'+host+':'+port+'/la',data=return_data("incomplete.json"))
		print("RETURN VALUE:"+json.loads(resp.text)["message"])
		assert resp.status_code == 500

	def test_TEXT_TRANSFORMATION_INCOMPLETE_INPUT(self):
		resp = requests.post('http://'+host+':'+port+'/tt',data=return_data("incomplete.json"))
		print("RETURN VALUE:"+json.loads(resp.text)["message"])
		assert resp.status_code == 500

	def test_QUERYING_INCOMPLETE_INPUT(self):
		resp = requests.post('http://'+host+':'+port+'/querying',data=return_data("incomplete.json"))
		print("RETURN VALUE:"+json.loads(resp.text)["message"])
		assert resp.status_code == 500	
	
	#------------------------------#
	# Common POST Tests -- Working #
	#------------------------------#	
	
	#Basic Server Checks
	def test_SERVER_INDEX_CHECK(self):
		resp = requests.get('http://'+host+':'+port)
		assert resp.status_code == 200

	#Crawling Checks
	def test_CRAWLING_BASIC_REDIRECT_INPUT(self):
		resp = requests.post('http://'+host+':'+port+'/crawling',data=return_data("crawling_input1.json"))
		assert resp.status_code == 200

	def test_CRAWLING_BASIC_DELETE_INPUT(self):
		resp = requests.post('http://'+host+':'+port+'/crawling',data=return_data("crawling_input2.json"))
		assert resp.status_code == 200

	#Link Analysis Checks
	def test_LINK_ANALYSIS_INPUT_1(self):
		resp = requests.post('http://'+host+':'+port+'/la',data=return_data("link_analysis_input1.json"))
		assert resp.status_code == 200

	def test_LINK_ANALYSIS_INPUT_2(self):
		resp = requests.post('http://'+host+':'+port+'/la',data=return_data("link_analysis_input2.json"))
		assert resp.status_code == 200

	#Text Transformation Checks
	def test_TEXT_TRANSFORMATION_INPUT_1(self):
		resp = requests.post('http://'+host+':'+port+'/tt',data=return_data("text_transformation1.json"))
		assert resp.status_code == 200

	def test_TEXT_TRANSFORMATION_INPUT_2(self): #Same as input two with additional N-GRAMS
		resp = requests.post('http://'+host+':'+port+'/tt',data=return_data("text_transformation2.json"))
		assert resp.status_code == 200

	def test_TEXT_TRANSFORMATION_INPUT_3(self): #Completely different website than INPUT 1/2
		resp = requests.post('http://'+host+':'+port+'/tt',data=return_data("text_transformation3.json"))
		assert resp.status_code == 200

	#Querying Checks
	def test_QUERYING_INPUT_1(self):
		resp = requests.post('http://'+host+':'+port+'/querying',data=return_data("querying1.json"))
		assert resp.status_code == 200

	#----------------------#
	# Incorrect Data Types #
	#----------------------#

	#Crawling Checks
	def test_CRAWLING_BASIC_INCORRECT_INPUT_1(self): #Redirect code is alpha characters
		resp = requests.post('http://'+host+':'+port+'/crawling',data=return_data("crawling_input_error1.json"))
		print("RETURN VALUE:"+json.loads(resp.text)["message"])
		assert resp.status_code == 500

	def test_CRAWLING_BASIC_INCORRECT_INPUT_2(self): #Attempt to redirect a non existant website? THIS SHOULD AT LEAST RETURN A WARNING MESSAGE.
		resp = requests.post('http://'+host+':'+port+'/crawling',data=return_data("crawling_input_error2.json"))
		assert resp.status_code == 200

	#def test_CRAWLING_BASIC_INCORRECT_INPUT_2(self): #Attempt to redirect to an already stored website? THIS RESULTS IN A PROBLEM AND WILL CAUSE CRASHES.
	#	resp = requests.post('http://'+host+':'+port+'/crawling',data=return_data("crawling_input_error3.json"))
	#	print("RETURN VALUE:"+json.loads(resp.text)["message"])
	#	assert resp.status_code == 500

	#Link Analysis Checks
	def test_LINK_ANALYSIS_INCORRECT_INPUT_1(self): #Ranking is alpha characters
		resp = requests.post('http://'+host+':'+port+'/la',data=return_data("link_analysis_input_error1.json"))
		assert resp.status_code == 500

	def test_LINK_ANALYSIS_INCORRECT_INPUT_2(self): #Input lists are uneven sizes
		resp = requests.post('http://'+host+':'+port+'/la',data=return_data("link_analysis_input_error2.json"))
		assert resp.status_code == 500

	#Text Transformation Checks
	def test_TEXT_TRANSFORMATION_BASIC_INCORRECT_INPUT_1(self): #Frequency is alpha characters
		resp = requests.post('http://'+host+':'+port+'/tt',data=return_data("text_transformation_error1.json"))
		assert resp.status_code == 200

	#Querying Checks
	def test_QUERYING_BASIC_INCORRECT_INPUT_1(self): #Querying requests SOME non existent information
		resp = requests.post('http://'+host+':'+port+'/querying',data=return_data("querying_error1.json"))
		assert len(json.loads(resp.text)["data"]) == 2
		assert len(json.loads(resp.text)["data"][0]) == 0
		assert len(json.loads(resp.text)["data"][1]) == 5
		assert resp.status_code == 200

	def test_QUERYING_BASIC_INCORRECT_INPUT_2(self): #Querying requests ONLY non existent information
		resp = requests.post('http://'+host+':'+port+'/querying',data=return_data("querying_error2.json"))
		assert len(json.loads(resp.text)["data"]) == 1
		assert len(json.loads(resp.text)["data"][0]) == 0
		assert resp.status_code == 200