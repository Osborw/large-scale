from flask import jsonify, request
from flask_restful import Resource, Api

class TextTransformation(Resource):
	
	def get(self):
		result = {}
		return jsonify(result)

	def post(self):
		"""
		{
			metadata: {
				url:string,
				title: string,
				description: string,
				keywords: string[],
				authors: string[]
			},
			text: {
				headings: string[],
				body: string[]
			},
			grams: [{
				gram: string,
				headingfreq: double,
				bodyfreq: double
			}]
		}
		"""
		#Connect to DB
		#Parse out data, insert into DB

		metadata = request.json["metadata"]
		text = request.json["text"]
		grams = request.json["grams"]

		result = {'status': 200}
		return jsonify(result)