from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import data

app = Flask(__name__)
api = Api(app)

api.add_resource(data.crawling.Crawling, '/crawling')
api.add_resource(data.text_transformation.TextTransformation, '/tt')
api.add_resource(data.link_analysis.LinkAnalysis, '/la')
api.add_resource(data.ranking.Ranking, '/ranking')
api.add_resource(data.querying.Querying, '/querying')

if __name__ == "__main__":
	app.run(debug=True)