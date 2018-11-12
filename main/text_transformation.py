from aiohttp import web
import psycopg2
import json

async def post(request):
	"""
	{
		"metadata": {
			"url": string,
			"title": string,
			"description": string,
			"keywords": string[],
			"authors": string[]
		},
		"text": {
			"headings": string[],
			"body": []
		},
		"grams": [{
			"gram": string,
			"headingfreq": double,
			"bodyfreq": double
		}]
	}
	"""
	try:
		request = await request.json()
		metadata = request["metadata"]
		text = request["text"]
		grams = request["grams"]

		response_obj = {"status": 200}
		return web.Response(text=json.dumps(response_obj), status=200)

	except Exception as e:
		response_obj = {"status": 500, "message": "Incorrect JSON Format: " + str(e)}
		return web.Response(text=json.dumps(response_obj), status=500)