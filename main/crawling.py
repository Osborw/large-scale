from aiohttp import web
import psycopg2
import json

async def post(request):
	"""
	{
		"url": string,
		"error_code": int,
		"redirect": string
	}
	"""
	try:
		request = await request.json()
		url = request["url"]
		error_code = request["error_code"]
		redirect = request["redirect"]

		response_obj = {"status": 200}
		return web.Response(text=json.dumps(response_obj), status=200)

	except Exception as e:
		response_obj = {"status": 500, "message": "Incorrect JSON Format: " + str(e)}
		return web.Response(text=json.dumps(response_obj), status=500)