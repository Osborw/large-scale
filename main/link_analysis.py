from flask import jsonify, request
from flask_restful import Resource, Api

class LinkAnalysis(Resource):
	
	def get(self):
		result = {}
		return jsonify(result)

	def post(self):
		"""
		{
			"url": string[],
			"pagerank": double[]
		}
		"""
		#Check to make sure data is formatted correctly
			#If there is an error, return {'status': 500}
		#Connect to DB
		#Parse out data, insert into DB

		#url = request.json["url"]
		#pagerank = request.json["pagerank"]

		result = {'status': 200}
		return jsonify(result)