from flask import jsonify, request
from flask_restful import Resource, Api
from json import dumps

class Ranking(Resource):
	
	def get(self):
		"""
			Work In Progress
			-- Giving direct access to DB might be dangerous, but sending back
				everything that matches with a word or ngram would be
				massive. We'll have to figure out this one
		"""
		result = {}
		return jsonify(result)