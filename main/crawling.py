from flask import jsonify, request
from flask_restful import Resource, Api
from json import dumps

class Crawling(Resource):

	def get(self):
		result = {}
		return jsonify(result)

	def post(self):
		"""
		{
			"url": string
			"error_code": int
			"redirect": string
		}
		"""
		#Connect to DB
		#Parse out data, insert into DB

		#url = request.json['url']
		#error_code = request.json['error_code']
		#redirect = request.json['redirect']

		result = {'status': 200}
		return jsonify(result)