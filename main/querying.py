from aiohttp import web
import psycopg2
import json

async def get(request):
	"""
	get ==>
	{
		"docId": string[]
	}

	response: ==>
	{
		"data":
		[
			{
				"docId": string,
				"url": string,
				"title": string,
				"header": string[],
				"body": string[]
			},
			...
		]
	}
	"""
	try:
		request = await request.json()
		docId = request["docId"]

		response_obj = {"status": 200}
		return web.Response(text=json.dumps(response_obj), status=200)

	except Exception as e:
		response_obj = {"status": 500, "message": "Incorrect JSON Format: " + str(e)}
		return web.Response(text=json.dumps(response_obj), status=500)