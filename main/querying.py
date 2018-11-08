from flask import jsonify, request
from flask_restful import Resource, Api

class Querying(Resource):
	
	def get(self):
		"""
		{
			docId: string[]
		}
		"""

		#Connect to docID DB
		#Grab all the docId matches and return in result

		"""
		result = {
			{
				docID: string,
				url: string,
				title: string,
				header: string[],
				body: string[]
			},
			...
		}
		"""

		docId = request.json['docId']

		result = {}
		return jsonify(result)